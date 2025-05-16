from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserInDB(UserBase):
    id: str
    hashed_password: str


class User(UserBase):
    id: str


class Token(BaseModel):
    token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None 