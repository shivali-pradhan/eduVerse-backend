from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from schemas.request_schemas import InstructorCreate, CourseCreate, ModuleCreate, QuizCreate, QuestionCreate
from schemas.response_schemas import InstructorResponse, InstructorCourseResponse, QuizBase
from repositories import instructor

router = APIRouter(
    prefix = "/instructors",
    tags = ["instructors"]
)

@router.get("/", response_model=List[InstructorResponse])
def list_instructors(db: Session = Depends(get_db)):
    return instructor.list_instructors(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorResponse)
def register_instructor(request: InstructorCreate, db: Session = Depends(get_db)):
    return instructor.register(request, db)

@router.get("/{id}", response_model=InstructorResponse)
def get_instructor(id: int, db: Session = Depends(get_db)):
    return instructor.get_instructor(id, db)

@router.get("/{id}/courses", response_model=List[InstructorCourseResponse])
def list_created_courses(id: int, db: Session = Depends(get_db)):
    return instructor.list_created_courses(id, db)
