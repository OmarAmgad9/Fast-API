from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import database, models, utils, schemas
from sqlalchemy.orm import Session
from ..database import get_db, engine



router = APIRouter(
    prefix='/user',
    tags=['user']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db:Session=Depends(get_db)):
    new_user = models.Users(**user.dict())
    new_user.password = utils.hash(user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # try:
    #     cursor.execute("INSERT INTO \"users\" (username, email, password) VALUES (%s, %s, %s) RETURNING *;", (user.username, user.email, user.password))
    #     new_user = cursor.fetchone()
    #     conn.commit()
    # except:
        
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    return new_user 

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This user with {id} Not Found")
    
    return user