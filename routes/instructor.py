from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from schemas.request_schemas import InstructorCreate, CourseCreate, ModuleCreate, QuizCreate, QuestionCreate
from schemas.response_schemas import InstructorResponse, InstructorCourseResponse, QuizBase
from repositories import instructor
from repositories.instructor import profile, course, quiz

router = APIRouter(
    prefix = "/instructors",
    tags = ["instructors"]
)

@router.get("/", response_model=List[InstructorResponse])
def list_instructors(db: Session = Depends(get_db)):
    return profile.list_all(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructorResponse)
def register_instructor(request: InstructorCreate, db: Session = Depends(get_db)):
    return profile.register(request, db)

@router.get("/{id}", response_model=InstructorResponse)
def get_instructor_profile(id: int, db: Session = Depends(get_db)):
    return profile.get_one(id, db)


''' Courses '''

@router.get("/{id}/courses", response_model=List[InstructorCourseResponse])
def list_created_courses(id: int, db: Session = Depends(get_db)):
    return course.list_created_courses(id, db)

@router.post("/{id}/courses", status_code=status.HTTP_201_CREATED, response_model=InstructorCourseResponse)
def create_course(id: int, request: CourseCreate, db: Session = Depends(get_db)):
    return course.create_course(id, request, db)

@router.put("/{i_id}/courses/{c_id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructorCourseResponse)
def update_course(i_id: int, c_id: int, request: CourseCreate, db: Session = Depends(get_db)):
    return course.update_course(i_id, c_id, request, db)

@router.delete("/{i_id}/courses/{c_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(i_id: int, c_id: int, db: Session = Depends(get_db)):
    return course.delete_course(i_id, c_id, db)


@router.post("/{i_id}/courses/{c_id}/modules", status_code=status.HTTP_201_CREATED)
def add_module(i_id: int, c_id: int, request: ModuleCreate, db: Session = Depends(get_db)):
    return course.add_module(i_id, c_id, request, db)

@router.put("/{i_id}/courses/{c_id}/modules/{m_id}", status_code=status.HTTP_202_ACCEPTED)
def update_module(i_id: int, c_id: int, m_id: int, request: ModuleCreate, db: Session = Depends(get_db)):
    return course.update_module(i_id, c_id, m_id, request, db)

@router.delete("/{i_id}/courses/{c_id}/modules/{m_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(i_id: int, c_id: int, m_id: int, request: ModuleCreate, db: Session = Depends(get_db)):
    return course.delete_module(i_id, c_id, m_id, request, db)




''' Quizzes '''

@router.get("/{i_id}/courses/{c_id}/modules/{m_id}/quizzes", response_model=QuizBase)
def list_quizzes(i_id: int, c_id: int, m_id: int, db: Session = Depends(get_db)):
    return quiz.list_quizzes(i_id, c_id, m_id, db)

@router.post("/{i_id}/courses/{c_id}/modules/{m_id}/quizzes", status_code=status.HTTP_201_CREATED)
def create_quiz(i_id: int, c_id: int, m_id: int, request: QuizCreate, db: Session = Depends(get_db)):
    return quiz.create_quiz(i_id, c_id, m_id, request, db)

@router.put("/{i_id}/courses/{c_id}/modules/{m_id}/quizzes/{q_id}", status_code=status.HTTP_202_ACCEPTED)
def update_quiz(i_id: int, c_id: int, m_id: int, q_id: int, request: QuizCreate, db: Session = Depends(get_db)):
    return quiz.update_quiz(i_id, c_id, m_id, q_id, request, db)

@router.delete("/{i_id}/courses/{c_id}/modules/{m_id}/quizzes/{q_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(i_id: int, c_id: int, m_id: int, q_id: int, db: Session = Depends(get_db)):
    return quiz.delete_quiz(i_id, c_id, m_id, q_id, db)

@router.post("/{i_id}/courses/{c_id}/modules/{m_id}/quizzes/{q_id}/questions", status_code=status.HTTP_201_CREATED)
def add_question(i_id: int, c_id: int, m_id: int, q_id: int, request: QuestionCreate, db: Session = Depends(get_db)):
    return quiz.add_question(i_id, c_id, m_id, q_id, request, db)