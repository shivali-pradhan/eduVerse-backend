from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from core.config import settings
from schemas.token_schemas import Token
from core.security import create_access_token, authenticate_user
from database import get_db


router = APIRouter(
    prefix = "/auth",
    tags = ["authentication"]
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = authenticate_user(username, password, db)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  
    access_token = create_access_token(data={"sub": user.username, "role": user.role, "exp": access_token_expires})
    
    return Token(access_token=access_token)
