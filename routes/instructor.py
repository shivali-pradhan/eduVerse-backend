from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from auth.dependencies import get_current_user, require_instructor
from schemas.request_schemas import InstructorCreate, InstructorUpdate, UserCreate
from schemas.response_schemas import InstructorBase, InstructorResponse, InstructorCourseResponse
from schemas.token_schemas import CurrentUser
from repositories import instructor

router = APIRouter(
    prefix = "/instructors",
    tags = ["instructors"]
)

@router.get("/", response_model=List[InstructorResponse])
def list_instructors(db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return instructor.list_instructors(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorBase)
def register_instructor(request: InstructorCreate, db: Session = Depends(get_db)):
    return instructor.register_instructor(request, db)

@router.get("/{id}", response_model=InstructorResponse)
def get_instructor(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return instructor.get_instructor(id, db)

@router.put("/{id}", response_model=InstructorBase)
def update_instructor(id: int, request: InstructorUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return instructor.update_instructor(id, request, db, current_user)


@router.get("/{id}/courses", response_model=List[InstructorCourseResponse])
def list_created_courses(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return instructor.list_created_courses(id, db)

@router.get("/{id}/quizzes")
def list_created_courses(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return instructor.list_created_quizzes(id, db, current_user)

@router.get("/{id}/quiz-results")
def show_quiz_results():
    return 
