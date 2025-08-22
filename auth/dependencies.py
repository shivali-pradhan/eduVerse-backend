from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from auth.security import decode_token
from database import get_db
from schemas.token_schemas import CurrentUser
from models.user_models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,  
        detail="Could not validate credentials",  
        headers={"WWW-Authenticate": "Bearer"},  
    )  

    token_data = decode_token(token, credentials_exception)
    username = token_data.sub

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user


def require_instructor(current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "INSTRUCTOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return current_user

def require_student(current_user: CurrentUser = Depends(get_current_user)):
    if current_user.role != "STUDENT":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return current_user
