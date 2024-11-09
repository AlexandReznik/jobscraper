from sqlalchemy.orm import Session

from . import models


def get_job(db: Session, event_id: int):
    """
    Retrieve a single job from the database by its ID.

    Args:
        db (Session): The database session.
        event_id (int): The ID of the job to retrieve.

    Returns:
        Job: The job instance with the specified ID, or None if not found.
    """
    return db.query(models.Job).filter(models.Job.id == event_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of jobs from the database with optional pagination.

    Args:
        db (Session): The database session.
        skip (int): The number of jobs to skip before starting to return results. Default is 0.
        limit (int): The maximum number of jobs to return. Default is 10.

    Returns:
        List[Job]: A list of job instances within the specified range.
    """
    return db.query(models.Job).offset(skip).limit(limit).all()