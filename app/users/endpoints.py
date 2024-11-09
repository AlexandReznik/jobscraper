from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.common import jwt
from app.common.database import get_db

from . import crud, schemas


router = APIRouter()


@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data to create, including email and password.
        db (Session): The database session dependency.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the email is already registered or an error occurs during creation.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")
    return created_user


@router.post("/me/", response_model=schemas.UserBase)
def read_users_me(
    current_user: Annotated[schemas.UserBase, Depends(crud.get_current_user)],
):
    """
    Retrieve the current authenticated user information.

    Args:
        current_user (UserBase): The current user, retrieved via the authentication dependency.

    Returns:
        UserBase: The authenticated user's base information.
    """
    return current_user


@router.post("/token/", response_model=schemas.UserToken)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.UserToken:
    """
    Authenticate the user and generate a JWT access token.

    Args:
        db (Session): The database session dependency.
        form_data (OAuth2PasswordRequestForm): The login form data containing username and password.

    Returns:
        UserToken: The generated JWT access token and token type.

    Raises:
        HTTPException: If authentication fails due to incorrect username or password.
    """
    user = crud.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)
    access_token = jwt.create_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return schemas.UserToken(access_token=access_token, token_type="bearer")


@router.put("/preferences/", response_model=schemas.UserPreferences)
def update_preferences(
    preferences: schemas.UserPreferences,
    current_user: schemas.UserBase = Depends(crud.get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the preferences of the current authenticated user.

    Args:
        preferences (UserPreferences): The new preferences data for the user.
        current_user (UserBase): The current authenticated user, retrieved via the authentication dependency.
        db (Session): The database session dependency.

    Returns:
        UserPreferences: The updated preferences for the user.
    """
    updated_preferences = crud.update_user_preferences(
        db=db,
        user=current_user,
        preferences=preferences
    )
    return updated_preferences