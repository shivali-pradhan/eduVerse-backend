from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models import Course, Module
from schemas.request_schemas import CourseCreate, ModuleCreate

from .profile import check_instructor


def check_course(i_id: int, c_id: int, db: Session):
    check_instructor(i_id, db)
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {c_id} created by instructor_id: {i_id}")


def list_created_courses(id: int, db: Session):
    instructor = check_instructor(id, db)
    return instructor.courses    # courses data with their modules and students enrolled


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
    course = check_course(i_id, c_id, db)

    course.name = request.name
    course.description = request.description
    course.credits = request.credits

    db.commit()
    db.refresh(course)

    return course


def delete_course(i_id: int, c_id: int, db: Session):
    check_instructor(i_id, db)
    
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such course with id: {c_id} created by instructor with id: {i_id}")
    
    course.delete(synchronize_session=False)
    db.commit()

    return "deleted"


def add_module(i_id: int, c_id: int, request: ModuleCreate, db: Session):
    check_course(i_id, c_id, db)

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

def update_module(i_id: int, c_id: int, m_id: int, request: ModuleCreate, db: Session):
    check_course(i_id, c_id, db)

    module = db.query(Module).filter(Module.id == m_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such module with id: {m_id} in course with id: {c_id}")
    
    module.name = request.name
    module.description = request.description
    
    db.commit()
    db.refresh(module)

    return module


def delete_module(i_id: int, c_id: int, m_id: int, db: Session):
    check_course(i_id, c_id, db)

    module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id)
    if not module.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such module with id: {m_id} in course with id: {c_id}")
    
    module.delete(synchronize_session=False)
    db.commit()

    return "deleted"
