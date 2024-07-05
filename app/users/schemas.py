from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    preferences: str
    
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int