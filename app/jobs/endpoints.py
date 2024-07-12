from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.common.database import get_db
from . import crud, schemas
from typing import List
from app.users.crud import get_current_user
from app.users.schemas import UserBase
from app.common.email_utils import send_email
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_scraper.spiders.djinni import DjinniSpider
from job_scraper.spiders.dou import DouSpider
from job_scraper.spiders.lhh import LhhSpider


router = APIRouter()


def run_scrapy_spiders():
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(DjinniSpider)
    process.crawl(DouSpider)
    process.crawl(LhhSpider)
    process.start()


def filter_jobs(jobs: List[schemas.JobBase], preferences: str) -> List[schemas.JobBase]:
    user_preferences = preferences.split(',')
    return [job for job in jobs if job.meets_preferences(user_preferences)]


def construct_email_body(jobs: List[schemas.JobBase]) -> str:
    return "\n\n".join([f"{job.title} in {job.location} - {job.url}" for job in jobs])


def send_jobs_email(jobs: List[schemas.JobBase], user_email: str):
    subject = "New Job Listings Based on Your Preferences"
    body = construct_email_body(jobs)
    try:
        send_email(subject, body, user_email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
    

@router.get("/all/", response_model=List[schemas.Job])
def read_events(skip: int = 0, limit: int = 50, 
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs
    

@router.get("/alert/", response_model=list[schemas.JobBase])
def scrape_and_get_jobs(db: Session = Depends(get_db), 
                        current_user: UserBase = Depends(get_current_user)):
    run_scrapy_spiders()
    jobs = crud.get_jobs(db, skip=0, limit=1000)
    filtered_jobs = filter_jobs(jobs, current_user.preferences)
    if not filtered_jobs:
        return {"message": "No jobs found based on user preferences"}
    send_jobs_email(filtered_jobs, current_user.email)
    return filtered_jobs