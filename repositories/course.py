from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.course_models import Course
from schemas.request_schemas import CourseCreate, CourseUpdate

from .instructor import check_instructor


def check_instructor_course(i_id: int, c_id: int, db: Session):
    check_instructor(i_id, db)
    course = db.query(Course).filter(Course.id == c_id, Course.instructor_id == i_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {c_id} created by instructor_id: {i_id}")


def list_all_courses(db: Session):
    all_courses = db.query(Course).all()
    return all_courses

def get_course(id: int, db: Session):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {id}")
    return course


def create_course(request: CourseCreate, db: Session):
    check_instructor(request.instructor_id, db)
    
    new_course = Course(
        name = request.name,
        description = request.description,
        credits = request.credits,
        created_at = datetime.datetime.now(),
        instructor_id = request.instructor_id
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

### Authorization required ###
def update_course(id: int, request: CourseUpdate, db: Session):
    
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {id}")
    
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

