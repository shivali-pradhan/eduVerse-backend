from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from models import Course, Module
from my_schemas.response_schemas import CourseResponse

from database import get_db

router = APIRouter(
    prefix = "/courses",
    tags = ["courses"]
)


@router.get("/", response_model=List[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    all_courses = db.query(Course).all()
    return all_courses

@router.get("/{id}", response_model=CourseResponse)
def get_course_(id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {id}")
    return course


@router.get("/{c_id}/modules/{m_id}")
def get_module(c_id: int, m_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == c_id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {c_id}")
    
    module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {m_id} in course_id: {c_id}")
    
    return module
