import os
from datetime import datetime, timedelta, timezone
from typing import Union

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import JWTError, jwt

from app.common.oauth2 import oauth2_scheme

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

if not SECRET_KEY or not ALGORITHM:
    raise EnvironmentError("Environment variables SECRET_KEY and ALGORITHM must be set")


def create_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Creates a JWT token with the specified data and expiration time.

    Args:
        data (dict): The data to encode in the JWT token.
        expires_delta (Union[timedelta, None], optional): 
            The duration for which the token is valid. 
            If None, the token expires in 15 minutes by default.

    Returns:
        str: The encoded JWT token as a string.

    Raises:
        EnvironmentError: If SECRET_KEY or ALGORITHM environment variables are not set.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str = Depends(oauth2_scheme)):
    """
    Decodes and validates the JWT token from the request.

    Args:
        token (str): The JWT token to decode, typically provided by the OAuth2 scheme.

    Returns:
        dict: The decoded JWT payload if the token is valid.

    Raises:
        HTTPException: If the JWT token is invalid or expired, raises a 401 Unauthorized error.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")