from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.token_schemas import CurrentUser
from auth.dependencies import get_current_user
from database import get_db
from models.user_models import Instructor, Student

router = APIRouter(
    prefix = "/users", 
    tags = ["users"]
)

@router.get("/current")
def get_user(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    user = {}
    if current_user.role == "INSTRUCTOR":
        instructor = db.query(Instructor).filter(Instructor.id == current_user.id).first()
        user = {
            "role": current_user.role,
            "first_name": instructor.first_name,
            "last_name": instructor.last_name,
            "email": instructor.email,
            "qualification": instructor.qualification
        }
    elif current_user.role == "STUDENT":
        student = db.query(Student).filter(Student.id == current_user.id).first()
        user = {
            "role": current_user.role,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
        }
    return { "user": user }