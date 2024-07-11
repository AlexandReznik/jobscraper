from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    preferences: str
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserPreferences(BaseModel):
    preferences: str


class User(UserBase):
    id: int


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str