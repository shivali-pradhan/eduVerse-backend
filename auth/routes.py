from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from core.config import settings
from schemas.token_schemas import Token
from auth.security import create_access_token, authenticate_user
from database import get_db
from models.user_models import Instructor, Student


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
    
    if user.role == "INSTRUCTOR":
        instructor = db.query(Instructor).filter(Instructor.id == user.id).first()
        current_user = {
            "first_name": instructor.first_name,
            "last_name": instructor.last_name,
            "email": instructor.email,
        }
    elif user.role == "STUDENT":
        student = db.query(Student).filter(Student.id == user.id).first()
        current_user = {
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
        }

    logged_in_user = {
        "user": { **current_user,
            "role": user.role
        },
        "token": Token(access_token=access_token)
    }
    return logged_in_user
