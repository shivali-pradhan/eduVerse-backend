from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from auth.dependencies import require_instructor, require_student
from schemas.request_schemas import StudentCreate, EnrollmentCreate
from schemas.response_schemas import StudentBase, StudentResponse, StudentCourseResponse
from schemas.token_schemas import CurrentUser
from repositories import student

router = APIRouter(
    prefix = "/students", 
    tags = ["students"]
)

@router.get("/", response_model=List[StudentBase])
def list_students(db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return student.list_students(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentBase)
def register_student(request: StudentCreate, db: Session = Depends(get_db)):
    return student.register_student(request, db)

@router.get("/{id}", response_model=StudentResponse)
def get_student(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.get_student(id, db, current_user)


''' Courses '''

@router.get("/{id}/courses", response_model=List[StudentCourseResponse])
def list_enrolled_courses(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.list_enrolled_courses(id, db, current_user)

@router.post("/{id}/enroll")
def enroll_in_course(id: int, request: EnrollmentCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.enroll_in_course(id, request, db, current_user)

@router.get("/{id}/quizzes")
def list_available_quizzes(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.list_available_quizzes(id, db, current_user)

@router.get("/{id}/quiz-scores")
def show_quiz_scores():
    return



