from fastapi import Depends, APIRouter, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils, Oauth


router = APIRouter(
    tags=['authencation']
)

@router.post("/login")
def login(user_data:OAuth2PasswordRequestForm=Depends() ,db:Session=Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email==user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"This email or password Not correct")
    
    if not utils.varify(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This Password Not Correct")

    token = Oauth.create_access_token(data={"user_id":user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
    }