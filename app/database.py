from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
import psycopg2
import time

SQLACHEMY_DATABASE_URL = "postgresql://postgres:Omar1234567890@localhost/fastapi"

engine = create_engine(SQLACHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


while True:
    try:
        conn = psycopg2.connect(host="localhost", user="postgres", database='fastapi', 
                                password="Omar1234567890", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DATABASE Connetion was Successfully")
        break
    except:
        print("Can't connection with DATABASE")
        time.sleep(2)


