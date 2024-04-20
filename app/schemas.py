from pydantic import BaseModel
from datetime import datetime


class BasePost(BaseModel):
    title: str
    content: str

class UpdatePost(BasePost):
    pass

class Post(BasePost):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True