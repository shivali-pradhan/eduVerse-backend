from fastapi import APIRouter, status, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
from auth.dependencies import require_instructor, require_student
from schemas.request_schemas import StudentCreate, EnrollmentCreate, StudentUpdate
from schemas.response_schemas import StudentBase, StudentResponse, StudentCourseResponse, StudentQuizResponse, StudentQuizScoreResponse, StudentQuizAttemptResponse
from schemas.token_schemas import CurrentUser
from schemas.custom_pagination import PaginatedResponse
from services import student

router = APIRouter(
    prefix = "/students", 
    tags = ["students"]
)

@router.get("/", response_model=PaginatedResponse[StudentBase])
def list_students(
        search: Optional[str] = Query(None, description="Search by 'first_name', 'last_name' or 'email'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        page_num: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db), 
        current_user: CurrentUser = Depends(require_instructor)
    ):
    return student.list_students(db, search, sort_by, order, page_num, page_size)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=StudentBase)
def register_student(request: StudentCreate, db: Session = Depends(get_db)):
    return student.register_student(request, db)

@router.get("/{id}", response_model=StudentResponse)
def get_student(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.get_student(id, db, current_user)

@router.put("/{id}", response_model=StudentResponse)
def update_student(id: int, request: StudentUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.update_student(id, request, db, current_user)

''' Courses '''

@router.get("/{id}/courses", response_model=PaginatedResponse[StudentCourseResponse])
def list_enrolled_courses(id: int, 
        search: Optional[str] = Query(None, description="Search by 'name'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        page_num: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db), 
        current_user: CurrentUser = Depends(require_student)):
    return student.list_enrolled_courses(id, db, current_user, search, sort_by, order, page_num, page_size)

@router.post("/{id}/enroll")
def enroll_in_course(id: int, request: EnrollmentCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return student.enroll_in_course(id, request, db, current_user)


''' Quizzes '''

@router.get("/{id}/quizzes", response_model=PaginatedResponse[StudentQuizResponse])
def list_available_quizzes(
        id: int, 
        search: Optional[str] = Query(None, description="Search by 'title'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"), 
        page_num: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db), 
        current_user: CurrentUser = Depends(require_student)
    ):
    return student.list_available_quizzes(id, db, current_user, search, sort_by, order, page_num, page_size)

@router.get("/{id}/quiz-scores", response_model=PaginatedResponse[StudentQuizScoreResponse])
def show_quiz_scores(id: int, 
        page_num: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50), 
        db: Session = Depends(get_db), 
        current_user: CurrentUser = Depends(require_student)
    ):
    return student.show_quiz_scores(id, db, current_user, page_num, page_size)

# @router.get("/{id}/quiz-attempts", response_model=Page[StudentQuizAttemptResponse])
# def show_quiz_attempts(id: int, params: CustomParams = Depends(), db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
#     return paginate(student.show_quiz_attempts(id, db, current_user), params)



