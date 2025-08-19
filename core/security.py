from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt, JWTError

from models.user_models import User
from .config import settings
from schemas.token_schemas import TokenData


pwd_context = CryptContext(schemes=["bcrypt"])

class Hasher():

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Username")
 
    if not Hasher.verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    
    return user
    

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) 
    return encoded_jwt


def decode_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, role=role)
        return token_data
    
    except JWTError:
        raise credentials_exception