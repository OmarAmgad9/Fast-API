from pydantic import BaseModel, EmailStr
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str

class UpdatePost(BasePost):
    pass

class Post(BasePost):
    id: int
    # title: str
    # created_at: datetime

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    
    username: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    id: int
    username: str
    email : EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

