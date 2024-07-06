from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.common.database import get_db
from . import crud, schemas
from typing import List

router = APIRouter()


@router.get("/all/", response_model=List[schemas.Job])
def read_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs