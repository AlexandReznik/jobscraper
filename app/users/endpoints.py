from fastapi import APIRouter, Depends, HTTPException
from . import schemas, crud
from sqlalchemy.orm import Session
from typing import List
from app.common.database import get_db

router = APIRouter()


@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")
    return created_user


@router.get("/all/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users