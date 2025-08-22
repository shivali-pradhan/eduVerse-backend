from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user_models import User, Student
from models.course_models import Enrollment, Course, Module
from models.quiz_models import Quiz, QuizResult, QuizAttempt, Question
from schemas.request_schemas import StudentCreate, EnrollmentCreate, StudentUpdate
from schemas.token_schemas import CurrentUser
from auth.security import Hasher
from core.sort import sort

def check_student(id: int, db: Session, current_student: CurrentUser):
    if current_student.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student

def list_students(db: Session, search: str, sort_by: str, order: str):
    query = db.query(Student)

    if search:
        query = query.filter(
            Student.first_name.ilike(f"%{search}%") |
            Student.last_name.ilike(f"%{search}%") |
            Student.email.ilike(f"%{search}%") 
        )

    fields = ["id", "first_name", "last_name", "email", "created_at"]
    sorted_students = sort(query=query, model=Student, model_fields=fields, sort_field=sort_by, order=order)
        
    return sorted_students


def register_student(request: StudentCreate, db: Session):
    
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_user = User(
        username = request.username,
        password = hashed_password,
        role = "STUDENT"
    )
    db.add(new_user)
    db.flush()
    
    new_student = Student(
        id = new_user.id,
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_student(id: int, db: Session, current_student: CurrentUser):
    return check_student(id, db, current_student)

def update_student(id: int, db: Session, request: StudentUpdate, current_student: CurrentUser):
    student = check_student(id, db, current_student)

    student.first_name = request.first_name
    student.last_name = request.last_name
    student.email = request.email

    db.commit()
    db.refresh(student)

    return student


def list_enrolled_courses(id: int, db: Session, current_student: CurrentUser, search: str, sort_by: str, order: str):
    student = check_student(id, db, current_student)
    query = db.query(Course).join(Enrollment, Enrollment.course_id == Course.id & Enrollment.student_id == student.id)

    if search:
        query = query.filter(
            Course.name.ilike(f"%{search}%")
        )

    fields = ["id", "name", "credits", "duration"]
    sorted_courses = sort(sort(query=query, model=Course, model_fields=fields, sort_field=sort_by, order=order))

    return sorted_courses


def enroll_in_course(id: int, request: EnrollmentCreate, db: Session, current_student: CurrentUser):
    check_student(id, db, current_student)

    course = db.query(Course).filter(Course.id == request.course_id).first()
    if not course:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No course with id: {request.course_id}")
    
    new_enrollment = Enrollment(
        student_id = id,
        course_id = request.course_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


def list_available_quizzes(id: int, db: Session, current_student: CurrentUser, search: str, sort_by: str, order: str):
    student = check_student(id, db, current_student)

    course_ids = db.query(Enrollment.course_id).filter(Enrollment.student_id == student.id).all()
    if not course_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No course enrolled")
    
    enrolled_course_ids = []
    for item in course_ids:
        enrolled_course_ids.append(item[0])

    module_ids = db.query(Module.id).filter(Module.course_id.in_(enrolled_course_ids)).all()
    if not module_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No modules in enrolled courses")
    
    enrolled_module_ids = []
    for item in module_ids:
        enrolled_module_ids.append(item[0])

    query = db.query(Quiz).filter(Quiz.module_id.in_(enrolled_module_ids))
    
    if search:
        query = query.filter(
            Quiz.title.ilike(f"%{search}%") 
        )
    fields = ["id", "title", "marks_per_ques", "total_marks"]
    sorted_quizzes = sort(sort(query=query, model=Quiz, model_fields=fields, sort_field=sort_by, order=order))
    
    return sorted_quizzes


def show_quiz_scores(id: int, db: Session, current_student: CurrentUser):
    student = check_student(id, db, current_student)
    
    quiz_results = db.query(QuizResult.quiz_id, QuizResult.score).filter(QuizResult.student_id == student.id).all()
    if not quiz_results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No attempted quizzes")
    
    return quiz_results


def show_quiz_attempts(id: int, db: Session, current_student: CurrentUser):
    student = check_student(id, db, current_student)
    quiz_attempts = db.query(
        QuizAttempt.quiz_id, 
        QuizAttempt.question_id, 
        QuizAttempt.answer,
        Question.correct_option_id
        ).join(Question, Question.id == QuizAttempt.question_id).filter(
            QuizAttempt.student_id == student.id).all()
    if not quiz_attempts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No attempted quizzes")

    print(quiz_attempts)
    return quiz_attempts
    