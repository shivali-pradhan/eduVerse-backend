from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user_models import User, Instructor
from schemas.request_schemas import InstructorCreate, InstructorUpdate
from schemas.token_schemas import CurrentUser
from core.security import Hasher


def check_instructor(id: int, db: Session, current_instructor: CurrentUser):
    if current_instructor.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
    return instructor


def list_instructors(db: Session):
    instructors = db.query(Instructor).all()
    return instructors


def register_instructor(request: InstructorCreate, db: Session):
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_user = User(
        username = request.username,
        password = hashed_password,
        role = "INSTRUCTOR"
    )
    db.add(new_user)
    db.flush()

    new_instructor = Instructor(
        id = new_user.id,
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email,
        qualification = request.qualification
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)

    return new_instructor


def get_instructor(id: int, db: Session):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")

    return instructor

def update_instructor(id: int, request: InstructorUpdate, db: Session, current_user: CurrentUser):
    instructor = check_instructor(id, db, current_user)
    
    instructor.first_name = request.first_name
    instructor.last_name = request.last_name
    instructor.qualification = request.qualification
    instructor.email = request.email

    db.commit()
    db.refresh(instructor)

    return instructor


def list_created_courses(id: int, db: Session):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
    return instructor.courses


def list_created_quizzes(id: int, db: Session, current_instructor: CurrentUser):
    instructor = check_instructor(id, db, current_instructor)
