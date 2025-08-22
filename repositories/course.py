from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.course_models import Course
from schemas.request_schemas import CourseCreate, CourseUpdate
from schemas.token_schemas import CurrentUser
from .instructor import check_instructor
from core.sort import sort


def check_instructor_course(c_id: int, db: Session, current_instructor: CurrentUser):
    course = db.query(Course).filter(Course.id == c_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {c_id}")
    
    check_instructor(course.instructor_id, db, current_instructor)

    return course


def list_all_courses(db: Session, search: str, sort_by: str, order: str):
    query = db.query(Course)
    if search:
        query = query.filter(
            Course.name.ilike(f"%{search}%")
        )

    fields = ["id", "name", "credits", "duration"]
    sorted_courses = sort(sort(query=query, model=Course, model_fields=fields, sort_field=sort_by, order=order))

    return sorted_courses


def get_course(id: int, db: Session):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {id}")
    return course


def create_course(request: CourseCreate, db: Session, current_instructor: CurrentUser):
    check_instructor(request.instructor_id, db, current_instructor)
    
    new_course = Course(
        name = request.name,
        description = request.description,
        duration = 0,
        credits = request.credits,
        instructor_id = request.instructor_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course


def update_course(id: int, request: CourseUpdate, db: Session, current_instructor: CurrentUser):
    
    course = check_instructor_course(id, db, current_instructor)
    
    course.name = request.name
    course.description = request.description
    course.credits = request.credits

    db.commit()
    db.refresh(course)

    return course


def delete_course(id: int, db: Session, current_instructor: CurrentUser):
    course = check_instructor_course(id, db, current_instructor)
    db.delete(course)
    db.commit()

    return None

