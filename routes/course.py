from fastapi import APIRouter, Depends, status, Query
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas.request_schemas import CourseCreate
from schemas.response_schemas import InstructorCourseResponse, StudentCourseResponse
from schemas.token_schemas import CurrentUser
from repositories import course
from auth.dependencies import get_current_user, require_instructor
from database import get_db

router = APIRouter(
    prefix = "/courses",
    tags = ["courses"]
)


@router.get("/", response_model=Page[StudentCourseResponse])
def list_all_courses(
        search: Optional[str] = Query(None, description="Search by 'name'"),
        sort_by: Optional[str] = Query("id", description="Field to sort by"),
        order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
        params: Params = Depends(), 
        db: Session = Depends(get_db)
    ):
    return paginate(course.list_all_courses(db, search, sort_by, order), params)

@router.get("/{id}", response_model=StudentCourseResponse)
def get_course(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    return course.get_course(id, db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorCourseResponse)
def create_course(request: CourseCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.create_course(request, db, current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructorCourseResponse)
def update_course(id: int, request: CourseCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.update_course(id, request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return course.delete_course(id, db, current_user)


