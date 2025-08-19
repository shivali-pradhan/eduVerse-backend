from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from schemas.request_schemas import CourseCreate
from schemas.response_schemas import CourseResponse, InstructorCourseResponse, StudentCourseResponse
from repositories import course

from database import get_db

router = APIRouter(
    prefix = "/courses",
    tags = ["courses"]
)


@router.get("/", response_model=List[StudentCourseResponse])
def list_all_courses(db: Session = Depends(get_db)):
    return course.list_all_courses(db)

@router.get("/{id}", response_model=StudentCourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    return course.get_course(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorCourseResponse)
def create_course(request: CourseCreate, db: Session = Depends(get_db)):
    return course.create_course(request, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructorCourseResponse)
def update_course(id: int, request: CourseCreate, db: Session = Depends(get_db)):
    return course.update_course(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db)):
    return course.delete_course(id, db)


