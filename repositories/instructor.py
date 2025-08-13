from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models import Instructor, Course, Module
from schemas.request_schemas import InstructorCreate, CourseCreate, ModuleCreate
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
    instructor = check_instructor(id, db)
    return instructor

# def update(id: int, request: InstructorCreate, db: Session):
#     instructor = db.query(Instructor).filter(Instructor.id == id)
#     if not instructor.first():     
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
#     instructor.update(request)
#     db.commit()
#     db.refresh(instructor)
    
#     return instructor


''' Courses '''

def list_created_courses(id: int, db: Session):
    instructor = check_instructor(id, db)
    return instructor.courses


def create_course(id: int, request: CourseCreate, db: Session):
    instructor = check_instructor(id, db)
    
    new_course = Course(
        name = request.name,
        description = request.description,
        credits = request.credits,
        created_at = datetime.datetime.now(),
        instructor_id = id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    db.refresh(instructor)

    return new_course

def update_course(i_id: int, c_id: int, request: CourseCreate, db: Session):
    instructor = check_instructor(id, db)
    
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such course with id: {c_id} created by instructor with id: {i_id}")
    
    course.name = request.name
    course.description = request.description
    db.commit()
    db.refresh(course)

    return course

def delete_course(i_id: int, c_id: int, db: Session):
    instructor = check_instructor(id, db)
    
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such course with id: {c_id} created by instructor with id: {i_id}")
    
    course.delete(synchronize_session=False)
    db.commit()

    return "deleted"

def add_module(i_id: int, c_id: int, request: ModuleCreate, db: Session):
    instructor = check_instructor(id, db)
    
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such course with id: {c_id} created by instructor with id: {i_id}")
    
    new_module = Module(
        name = request.name,
        description = request.description,
        created_at = datetime.datetime.now(),
        course_id = c_id
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)

    return new_module







