from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """
    Base model for a user containing core user information.

    Attributes:
        email (EmailStr): The user's email address.
        preferences (str): The user's preferences as a string.
    """
    email: EmailStr
    preferences: str
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Model for creating a new user, extending the base user model to include a password.

    Attributes:
        password (str): The user's password.
    """
    password: str


class UserPreferences(BaseModel):
    """
    Model for updating or displaying user preferences.

    Attributes:
        preferences (str): The user's preferences.
    """
    preferences: str


class User(UserBase):
    """
    Model representing a user with an ID and basic user information.

    Attributes:
        id (int): The unique identifier for the user.
    """
    id: int


class UserToken(BaseModel):
    """
    Model for an authentication token issued to a user.

    Attributes:
        access_token (str): The token provided to the user for authentication.
        token_type (str): The type of token (e.g., "Bearer").
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model for holding the email associated with a token for verification or decoding.

    Attributes:
        email (str): The email associated with the token.
    """
    email: str