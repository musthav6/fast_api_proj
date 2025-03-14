from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    text: str

class Post(BaseModel):
    id: int
    text: str
    user_id: int

    class Config:
        orm_mode = True
