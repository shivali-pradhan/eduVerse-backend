from fastapi import APIRouter, status, Depends
from fastapi_pagination import Page, Params, paginate
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
from auth.dependencies import get_current_user, require_instructor
from schemas.request_schemas import InstructorCreate, InstructorUpdate
from schemas.response_schemas import InstructorBase, InstructorResponse, InstructorCourseResponse, InstructorQuizResponse, InstructorQuizScoreResponse, InstructorQuizAttemptResponse
from schemas.token_schemas import CurrentUser
from repositories import instructor
from fastapi import Query

router = APIRouter(
    prefix = "/instructors",
    tags = ["instructors"]
)

class MyCustomParams(Params):
    size: int = 10 

def get_custom_params(page: int = Query(1, ge=1), size: int = Query(20, ge=1, le=50)):
    return Params(page=page, size=size)


@router.get("/", response_model=Page[InstructorResponse])
def list_instructors(
        search: Optional[str] = Query(None, description="Search by 'first_name', 'last_name', 'email' or 'qualification'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        params: Params = Depends(), 
        db: Session = Depends(get_db)
    ):
    return paginate(instructor.list_instructors(db, search, sort_by, order), params)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorBase)
def register_instructor(request: InstructorCreate, db: Session = Depends(get_db)):
    return instructor.register_instructor(request, db)

@router.get("/{id}", response_model=InstructorResponse)
def get_instructor(id: int, db: Session = Depends(get_db)):
    return instructor.get_instructor(id, db)

@router.put("/{id}", response_model=InstructorBase)
def update_instructor(id: int, request: InstructorUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return instructor.update_instructor(id, request, db, current_user)


@router.get("/{id}/courses", response_model=Page[InstructorCourseResponse])
def list_created_courses(
        id: int, 
        search: Optional[str] = Query(None, description="Search by 'name'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        params: Params = Depends(), 
        db: Session = Depends(get_db)
    ):
    return paginate(instructor.list_created_courses(id, db, search, sort_by, order), params)

@router.get("/{id}/quizzes", response_model=Page[InstructorQuizResponse])
def list_created_quizzes(
        id: int,
        search: Optional[str] = Query(None, description="Search by 'title'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"), 
        params: Params = Depends(), db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return paginate(instructor.list_created_quizzes(id, db, current_user, search, sort_by, order), params)

@router.get("/{id}/quiz-results", response_model=Page[InstructorQuizScoreResponse])
def show_quiz_results(id: int, params: Params = Depends(), db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return paginate(instructor.show_quiz_results(id, db, current_user), params)

@router.get("/{id}/quiz-attempts", response_model=List[InstructorQuizAttemptResponse])
def show_quiz_attempts(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return instructor.show_quiz_attempts(id, db, current_user)
