import pandas as pd
from sqlalchemy.orm import Session
from app.common.database import SessionLocal
from app.jobs import crud as job_crud
from app.users import crud as user_crud
from app.common.email_utils import send_email
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_scraper.spiders.djinni import DjinniSpider
from job_scraper.spiders.dou import DouSpider
from job_scraper.spiders.lhh import LhhSpider


def run_scrapy_spiders():
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(DjinniSpider)
    process.crawl(DouSpider)
    process.crawl(LhhSpider)
    process.start()


def get_user_preferences(user_preferences):
    preferences = pd.read_json(user_preferences)
    return preferences


def filter_jobs_by_preferences(jobs, preferences):
    filtered_jobs = jobs
    for column, value in preferences.items():
        filtered_jobs = filtered_jobs[filtered_jobs[column].str.contains(value, na=False)]
    return filtered_jobs


def send_notifications():
    db: Session = SessionLocal()
    try:
        users = user_crud.get_users(db)
        jobs = job_crud.get_jobs(db, skip=0, limit=1000)
        jobs_df = pd.DataFrame([job.__dict__ for job in jobs])

        for user in users:
            preferences = get_user_preferences(user.preferences)
            filtered_jobs = filter_jobs_by_preferences(jobs_df, preferences)
            
            if not filtered_jobs.empty:
                body = "\n\n".join([f"{job['title']} at {job['company']} in {job['location']} - {job['url']}" for index, job in filtered_jobs.iterrows()])
                send_email("New Job Listings Based on Your Preferences", body, user.email)
    finally:
        db.close()

if __name__ == "__main__":
    run_scrapy_spiders()
    send_notifications()