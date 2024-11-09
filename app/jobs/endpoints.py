from typing import List

from fastapi import APIRouter, Depends, HTTPException
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.email_utils import send_email
from app.users.crud import get_current_user
from app.users.schemas import UserBase
from job_scraper.spiders.djinni import DjinniSpider
from job_scraper.spiders.dou import DouSpider
from job_scraper.spiders.lhh import LhhSpider

from . import crud, schemas


router = APIRouter()


def run_scrapy_spiders():
    """
    Start the Scrapy spiders to crawl job listings from multiple websites.
    """
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(DjinniSpider)
    process.crawl(DouSpider)
    process.crawl(LhhSpider)
    process.start()


def filter_jobs(jobs: List[schemas.JobBase], preferences: str) -> List[schemas.JobBase]:
    """
    Filter job listings based on user preferences.

    Args:
        jobs (List[schemas.JobBase]): List of job listings.
        preferences (str): Comma-separated string of user preferences.

    Returns:
        List[schemas.JobBase]: List of jobs that match the user's preferences.
    """
    user_preferences = preferences.split(',')
    return [job for job in jobs if job.meets_preferences(user_preferences)]


def construct_email_body(jobs: List[schemas.JobBase]) -> str:
    """
    Construct the body of the email containing job listings.

    Args:
        jobs (List[schemas.JobBase]): List of job listings.

    Returns:
        str: Email body text listing jobs with title, location, and URL.
    """
    return "\n\n".join([f"{job.title} in {job.location} - {job.url}" for job in jobs])


def send_jobs_email(jobs: List[schemas.JobBase], user_email: str):
    """
    Send an email to the user with job listings based on their preferences.

    Args:
        jobs (List[schemas.JobBase]): List of job listings to include in the email.
        user_email (str): The recipient's email address.

    Raises:
        HTTPException: If email sending fails.
    """
    subject = "New Job Listings Based on Your Preferences"
    body = construct_email_body(jobs)
    try:
        send_email(subject, body, user_email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    

@router.get("/all/", response_model=List[schemas.Job])
def read_jobss(skip: int = 0, limit: int = 50, 
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    """
    Retrieve a paginated list of jobs from the database.

    Args:
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.
        db (Session): Database session dependency.
        current_user (UserBase): The current authenticated user.

    Returns:
        List[schemas.Job]: List of jobs from the database.
    """
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs
    

@router.get("/alert/", response_model=list[schemas.JobBase])
def scrape_and_get_jobs(db: Session = Depends(get_db), 
                        current_user: UserBase = Depends(get_current_user)):
    """
    Run the job scraper, filter results by user preferences, and send an email alert.

    Args:
        db (Session): Database session dependency.
        current_user (UserBase): The current authenticated user.

    Returns:
        List[schemas.JobBase]: Filtered list of jobs matching user preferences,
        or a message if no matches are found.
    """
    run_scrapy_spiders()
    jobs = crud.get_jobs(db, skip=0, limit=1000)
    filtered_jobs = filter_jobs(jobs, current_user.preferences)
    if not filtered_jobs:
        return {"message": "No jobs found based on user preferences"}
    send_jobs_email(filtered_jobs, current_user.email)
    return filtered_jobs