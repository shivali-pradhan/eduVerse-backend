from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models import Instructor
from schemas.request_schemas import InstructorCreate
from hash import Hasher

def check_instructor(id: int, db: Session):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
    return instructor


def list_all(db: Session):
    instructors = db.query(Instructor).all()
    return instructors


def register(request: InstructorCreate, db: Session):
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_instructor = Instructor(
        first_name = request.first_name,
        last_name = request.last_name,
        username = request.username,
        password = hashed_password,
        email = request.email,
        role = "INSTRUCTOR",
        registered_at = datetime.datetime.now()
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)

    return new_instructor


def get_one(id: int, db: Session):
    return check_instructor(id, db)    # instructor data along with created courses data (no modules or students)


#### Update Instructor profile ####
