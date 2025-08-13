from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from my_schemas.request_schemas import InstructorCreate, CourseCreate, ModuleCreate
from my_schemas.response_schemas import InstructorResponse, InstructorCourseResponse
from repositories import instructor

router = APIRouter(
    prefix = "/instructors",
    tags = ["instructors"]
)

@router.get("/", response_model=List[InstructorResponse])
def list_instructors(db: Session = Depends(get_db)):
    return instructor.list_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorResponse)
def register_instructor(request: InstructorCreate, db: Session = Depends(get_db)):
    return instructor.register(request, db)

@router.get("/{id}", response_model=InstructorResponse)
def get_instructor_profile(id: int, db: Session = Depends(get_db)):
    return instructor.get_one(id, db)

# @router.put("/{id}")
# def update_instructor_profile(id: int, request: InstructorBase, db: Session = Depends(get_db)):
#     return instructor.update(id, request, db)


''' Courses '''

@router.get("/{id}/courses", response_model=List[InstructorCourseResponse])
def list_created_courses(id: int, db: Session = Depends(get_db)):
    return instructor.list_created_courses(id, db)

@router.post("/{id}/courses", status_code=status.HTTP_201_CREATED, response_model=InstructorCourseResponse)
def create_course(id: int, request: CourseCreate, db: Session = Depends(get_db)):
    return instructor.create_course(id, request, db)

@router.put("/{i_id}/courses/{c_id}", response_model=InstructorCourseResponse)
def update_course(i_id: int, c_id: int, request: CourseCreate, db: Session = Depends(get_db)):
    return instructor.update_course(i_id, c_id, request, db)

@router.post("/{i_id}/courses/{c_id}/modules", status_code=status.HTTP_201_CREATED)
def add_module(i_id: int, c_id: int, request: ModuleCreate, db: Session = Depends(get_db)):
    return instructor.add_module(i_id, c_id, request, db)


''' Quizzes '''




