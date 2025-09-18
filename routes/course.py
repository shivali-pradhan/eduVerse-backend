from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.request_schemas import CourseCreate
from schemas.response_schemas import CourseBase, InstructorCourseResponse, StudentCourseResponse
from schemas.token_schemas import CurrentUser
from services import course
from auth.dependencies import get_current_user, require_instructor
from database import get_db
from schemas.custom_pagination import PaginatedResponse

router = APIRouter(
    prefix = "/courses",
    tags = ["courses"]
)


@router.get("/", response_model=PaginatedResponse[StudentCourseResponse])
def list_all_courses(
        search: Optional[str] = Query(None, description="Search by 'name'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        page_num: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db)
    ):
    return course.list_all_courses(db, search, sort_by, order, page_num, page_size)

@router.get("/{id}", response_model=StudentCourseResponse)
def get_course(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return course.get_course(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CourseBase)
def create_course(request: CourseCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.create_course(request, db, current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructorCourseResponse)
def update_course(id: int, request: CourseCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.update_course(id, request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.delete_course(id, db, current_user)


