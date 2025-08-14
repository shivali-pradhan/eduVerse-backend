from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models import Student, Enrollment, Course, Module, Quiz
from schemas.request_schemas import StudentCreate, QuizAttempt
from hash import Hasher

def list_all(db: Session):
    students = db.query(Student).all()
    return students

def register(request: StudentCreate, db: Session):
    
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_student = Student(
        first_name = request.first_name,
        last_name = request.last_name,
        username = request.username,
        password = hashed_password,
        email = request.email,
        role = "STUDENT",
        registered_at = datetime.datetime.now()
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

def get_one(id: int, db: Session):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student


def list_enrolled_courses(id: int, db: Session):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student.enrolled_in



def enroll(s_id: int, c_id: int, db: Session):
    student = db.query(Student).filter(Student.id == s_id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {s_id}")
    
    course = db.query(Course).filter(Course.id == c_id).first()
    if not course:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {c_id}")
    
    new_enrollment = Enrollment(
        student_id = s_id,
        course_id = c_id,
        enrolled_at = datetime.datetime.now()
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


def attempt_quiz(s_id: int, c_id: int, m_id: int, q_id, request: QuizAttempt, db: Session):
    student = db.query(Student).filter(Student.id == s_id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {s_id}")
    
    is_course_enrolled = db.query(Enrollment).filter(Enrollment.student_id == s_id, Enrollment.course_id == c_id).first()
    if not is_course_enrolled:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course enrolled with id: {c_id}")
    
    module = db.query(Module).filter(Module.id == m_id).first()
    if not module:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {m_id}")
    
    quiz = db.query(Quiz).filter(Quiz.id == m_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {q_id} in module_id: {m_id}")
    
    attempts = []

    for attempt in request.question_answers:
        attempts.append(attempt)

    return attempts
    