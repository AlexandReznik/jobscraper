from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.database import get_db
from app.common.jwt import decode_token
from app.common.oauth2 import oauth2_scheme
from app.common.security import get_password_hash

from ..common.security import verify_password
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database with a hashed password.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user creation data schema.

    Returns:
        User: The created user instance if successful, otherwise None if there's an IntegrityError.
    """
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, 
                          preferences=user.preferences, 
                          password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        return None


def get_user(db: Session, user_id: int):
    """
    Retrieve a user from the database by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user instance if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of all user instances.
    """
    return db.query(models.User).all()


def authenticate_user(db: Session, email: str, password: str):
    """
    Verify the user's email and password to authenticate them.

    Args:
        db (Session): The database session.
        email (str): The email of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        User: The authenticated user instance if successful, otherwise None.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user from the database by their email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        User: The user instance if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the provided authentication token.

    Args:
        db (Session): The database session.
        token (str): The authentication token of the current user.

    Raises:
        HTTPException: If the token is invalid or the user could not be validated.

    Returns:
        User: The user instance associated with the token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except ValueError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


def update_user_preferences(db: Session, user: schemas.UserBase, 
                            preferences: schemas.UserPreferences):
    """
    Update a user's preferences in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserBase): The user whose preferences are to be updated.
        preferences (schemas.UserPreferences): The new preferences for the user.

    Returns:
        UserPreferences: The updated preferences.
    """
    user.preferences = preferences.preferences
    db.commit()
    db.refresh(user)
    return preferences