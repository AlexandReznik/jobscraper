from sqlalchemy.orm import Session
from . import models


def get_job(db: Session, event_id: int):
    return db.query(models.Job).filter(models.Job.id == event_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Job).offset(skip).limit(limit).all()