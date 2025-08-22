from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.user_models import User, Instructor
from models.course_models import Course, Module
from models.quiz_models import Quiz, QuizResult, QuizAttempt, Question
from schemas.request_schemas import InstructorCreate, InstructorUpdate
from schemas.token_schemas import CurrentUser
from auth.security import Hasher
from core.sort import sort


def check_instructor(id: int, db: Session, current_instructor: CurrentUser):
    if current_instructor.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
    return instructor

def filter_quiz_ids(id: int, db: Session, current_instructor: CurrentUser):
    instructor = check_instructor(id, db, current_instructor)

    course_ids = db.query(Course.id).filter(Course.instructor_id == instructor.id).all()
    if not course_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No course created")
    
    created_course_ids = []
    for item in course_ids:
        created_course_ids.append(item[0])

    module_ids = db.query(Module.id).filter(Module.course_id.in_(created_course_ids)).all()
    if not module_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No modules in created courses")
    
    created_module_ids = []
    for item in module_ids:
        created_module_ids.append(item[0])

    quiz_ids = db.query(Quiz.id).filter(Quiz.module_id.in_(created_module_ids)).all()
    if not quiz_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No quizzes created")
    
    created_quiz_ids = []
    for item in quiz_ids:
        created_quiz_ids.append(item[0])

    return created_quiz_ids


def list_instructors(db: Session, search: str, sort_by: str, order: str):
    query = db.query(Instructor)

    if search:
        query = query.filter(
            Instructor.first_name.ilike(f"%{search}%") |
            Instructor.last_name.ilike(f"%{search}%") |
            Instructor.email.ilike(f"%{search}%") |
            Instructor.qualification.ilike(f"%{search}%")
        )

    fields = ["id", "first_name", "last_name", "email", "qualification", "created_at"]
    sorted_instructors = sort(query=query, model=Instructor, model_fields=fields, sort_field=sort_by, order=order)
        
    return sorted_instructors
    


def register_instructor(request: InstructorCreate, db: Session):
    hashed_password = Hasher.get_password_hash(request.password)
    
    new_user = User(
        username = request.username,
        password = hashed_password,
        role = "INSTRUCTOR"
    )
    db.add(new_user)
    db.flush()

    new_instructor = Instructor(
        id = new_user.id,
        first_name = request.first_name,
        last_name = request.last_name,
        email = request.email,
        qualification = request.qualification
    )
    db.add(new_instructor)
    db.commit()
    db.refresh(new_instructor)

    return new_instructor


def get_instructor(id: int, db: Session):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")

    return instructor


def update_instructor(id: int, request: InstructorUpdate, db: Session, current_user: CurrentUser):
    instructor = check_instructor(id, db, current_user)
    
    instructor.first_name = request.first_name
    instructor.last_name = request.last_name
    instructor.qualification = request.qualification
    instructor.email = request.email

    db.commit()
    db.refresh(instructor)

    return instructor


def list_created_courses(id: int, db: Session, search: str, sort_by: str, order: str):
    instructor = db.query(Instructor).filter(Instructor.id == id).first()
    if not instructor:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No instructor with id: {id}")
    
    query = db.query(Course).filter(Course.instructor_id == instructor.id)

    if search:
        query = query.filter(
            Course.name.ilike(f"%{search}%")
        )

    fields = ["id", "name", "credits", "duration"]
    sorted_courses = sort(sort(query=query, model=Course, model_fields=fields, sort_field=sort_by, order=order))

    return sorted_courses


def list_created_quizzes(id: int, db: Session, current_instructor: CurrentUser, search: str, sort_by: str, order: str):
    created_quiz_ids = filter_quiz_ids(id, db, current_instructor)
    query = db.query(Quiz).filter(Quiz.id.in_(created_quiz_ids))

    if search:
        query = query.filter(
            Quiz.title.ilike(f"%{search}%") 
        )
    fields = ["id", "title", "marks_per_ques", "total_marks"]
    sorted_quizzes = sort(sort(query=query, model=Quiz, model_fields=fields, sort_field=sort_by, order=order))
    
    return sorted_quizzes


def show_quiz_results(id: int, db: Session, current_instructor: CurrentUser):
    created_quiz_ids = filter_quiz_ids(id, db, current_instructor)

    quiz_results = db.query(QuizResult).filter(QuizResult.quiz_id.in_(created_quiz_ids)).all()
    if not quiz_results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No quizzes attempted")

    return quiz_results


def show_quiz_attempts(id: int, db: Session, current_instructor: CurrentUser):
    created_quiz_ids = filter_quiz_ids(id, db, current_instructor)

    quiz_attempts = db.query(
        QuizAttempt.student_id, 
        QuizAttempt.quiz_id, 
        QuizAttempt.question_id, 
        QuizAttempt.answer, 
        Question.correct_option_id
        ).join(Question, Question.id == QuizAttempt.question_id).filter(QuizAttempt.quiz_id.in_(created_quiz_ids)).all()
    if not quiz_attempts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No quizzes attempted")

    return quiz_attempts