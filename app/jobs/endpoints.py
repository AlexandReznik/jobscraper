from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from . import crud, schemas
from typing import List
from app.users.crud import get_current_user
from app.users.schemas import UserBase
from app.common.email_utils import send_email

router = APIRouter()


@router.get("/all/", response_model=List[schemas.Job])
def read_events(skip: int = 0, limit: int = 50, 
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs


@router.get("/alert/", response_model=list[schemas.JobBase])
def scrape_and_get_jobs(db: Session = Depends(get_db), 
                        current_user: UserBase = Depends(get_current_user)):
    jobs = crud.get_jobs(db, skip=0, limit=1000)
    user_preferences = current_user.preferences
    filtered_jobs = [job for job in jobs if job.meets_preferences(user_preferences.split(','))]
    if filtered_jobs:
        body = "\n\n".join(
            [f"{job.title} in {job.location} - {job.url}"
             for job in filtered_jobs])
        try:
            send_email("New Job Listings Based on Your Preferences", body, current_user.email)
        except Exception as e:
            f"Failed to send email: {str(e)}"
    else:
        return "No jobs found based on user preferences"
    return filtered_jobs