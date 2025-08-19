from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.user_models import User, Student
from models.course_models import Enrollment, Course, Module
from models.quiz_models import Quiz, QuizAttempt
from schemas.request_schemas import StudentCreate, EnrollmentCreate
from core.security import Hasher


def list_students(db: Session):
    students = db.query(Student).all()
    return students

def register_student(request: StudentCreate, db: Session):
    
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_user = User(
        username = request.username,
        password = hashed_password,
        role = "STUDENT"
    )
    db.add(new_user)

    new_student = Student(
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_student(id: int, db: Session):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student


def list_enrolled_courses(id: int, db: Session):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student.enrolled_in


def enroll_in_course(id: int, request: EnrollmentCreate, db: Session):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")
    
    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {request.course_id}")
    
    new_enrollment = Enrollment(
        student_id = id,
        course_id = request.course_id,
        enrolled_at = datetime.datetime.now()
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


def attempt_quiz(s_id: int, c_id: int, m_id: int, q_id, db: Session):
    student = db.query(Student).filter(Student.id == s_id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {s_id}")
    
    is_course_enrolled = db.query(Enrollment).filter(Enrollment.student_id == s_id, Enrollment.course_id == c_id).first()
    if not is_course_enrolled:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course enrolled with id: {c_id}")
    
    module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id).first()
    if not module:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {m_id}")
    
    quiz = db.query(Quiz).filter(Quiz.id == m_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {q_id} in module_id: {m_id}")
    
    # attempts = []

    # for attempt in request.question_answers:

    #     print(attempt.question_id, attempt.option_id)

    #     new_quiz_attempt = QuizAttempt(
    #         student_id = s_id,
    #         quiz_id = q_id,
    #         question_id = attempt.question_id,
    #         answer = attempt.option_id
    #     )
    #     db.add(new_quiz_attempt)
    #     db.commit()
    #     db.refresh(new_quiz_attempt)

    #     attempts.append(attempt)

    new_quiz_attempt = QuizAttempt(
        student_id = 1,
        quiz_id = 1,
        question_id = 1,
        answer = 1
    )
    db.add(new_quiz_attempt)
    db.commit()
    db.refresh(new_quiz_attempt)        


    return "Added"
    