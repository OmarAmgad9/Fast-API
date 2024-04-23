from fastapi import FastAPI, status,Depends, HTTPException

from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

app.get("/")
def main_url():
    return {
        "message": "nothing in this path check /post",
    }
