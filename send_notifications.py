from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import Session

from app.common.database import SessionLocal
from app.common.email_utils import send_email
from app.jobs import crud as job_crud
from app.users import crud as user_crud
from job_scraper.spiders.djinni import DjinniSpider
from job_scraper.spiders.dou import DouSpider
from job_scraper.spiders.lhh import LhhSpider


def run_scrapy_spiders():
    """
    Run all configured Scrapy spiders for job scraping.

    This function initializes a CrawlerProcess with project settings
    and starts crawling with DjinniSpider, DouSpider, and LhhSpider.
    """
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(DjinniSpider)
    process.crawl(DouSpider)
    process.crawl(LhhSpider)
    process.start()


def get_user_preferences(user_preferences):
    """
    Parse user preferences from a comma-separated string.

    Args:
        user_preferences (str): A string containing comma-separated user preferences.

    Returns:
        List[str]: A list of cleaned, individual preferences.
    """
    preferences = [preference.strip() for preference in user_preferences.split(',')]
    return preferences


def filter_jobs_by_preferences(jobs, preferences):
    """
    Filter jobs by user preferences.

    Args:
        jobs (list): A list of job objects.
        preferences (list): A list of user preference strings.

    Returns:
        List: A list of job objects that meet user preferences.
    """
    filtered_jobs = []
    for job in jobs:
        if job.meets_preferences(preferences):
            filtered_jobs.append(job)
    return filtered_jobs


def send_notifications():
    """
    Send job notification emails to users based on their preferences.

    This function retrieves users and jobs from the database,
    filters the jobs based on each user's preferences, and sends an
    email notification if matching jobs are found.

    Closes the database session after sending notifications.
    """
    db: Session = SessionLocal()
    try:
        users = user_crud.get_users(db)
        jobs = job_crud.get_jobs(db, skip=0, limit=1000)

        for user in users:
            preferences = get_user_preferences(user.preferences)
            filtered_jobs = filter_jobs_by_preferences(jobs, preferences)

            if filtered_jobs:
                body = "\n\n".join(
                    [f"{job.title} - {job.url}"
                     for job in filtered_jobs])
                send_email("New Job Listings Based on Your Preferences", body, user.email)
    finally:
        db.close()


if __name__ == "__main__":
    run_scrapy_spiders()
    send_notifications()