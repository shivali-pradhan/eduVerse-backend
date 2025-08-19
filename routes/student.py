from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from schemas.request_schemas import StudentCreate, EnrollmentCreate
from schemas.response_schemas import StudentResponse, StudentCourseResponse
from repositories import student

router = APIRouter(
    prefix = "/students", 
    tags = ["students"]
)

@router.get("/", response_model=List[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    return student.list_students(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
def register_student(request: StudentCreate, db: Session = Depends(get_db)):
    return student.register_student(request, db)

@router.get("/{id}", response_model=StudentResponse)
def get_student(id: int, db: Session = Depends(get_db)):
    return student.get_student(id, db)



''' Courses '''

@router.get("/{id}/courses", response_model=List[StudentCourseResponse])
def list_enrolled_courses(id: int, db: Session = Depends(get_db)):
    return student.list_enrolled_courses(id, db)

@router.post("/{id}/enroll")
def enroll_in_course(id: int, request: EnrollmentCreate, db: Session = Depends(get_db)):
    return student.enroll_in_course(id, request, db)


''' Quizzes '''

@router.post("/{s_id}/courses/{c_id}/modules/{m_id}/quizzes/{q_id}")
def attempt_quiz(s_id: int, c_id: int, m_id: int, q_id, db: Session = Depends(get_db)):
    return student.attempt_quiz(s_id, c_id, m_id, q_id, db)


