from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str]
    bio: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]
    city: Optional[str]
    profession: Optional[str]
    interests: Optional[str]
    social_links: Optional[str]
