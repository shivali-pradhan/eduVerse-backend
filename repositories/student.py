from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user_models import User, Student
from models.course_models import Enrollment, Course
from schemas.request_schemas import StudentCreate, EnrollmentCreate
from schemas.token_schemas import CurrentUser
from core.security import Hasher

def check_student(id: int, db: Session, current_student: CurrentUser):
    if current_student.id != id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    student = db.query(Student).filter(Student.id == id).first()
    if not student:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No student with id: {id}")

    return student

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


def list_enrolled_courses(id: int, db: Session, current_student: CurrentUser):
    student = check_student(id, db, current_student)
    return student.enrolled_in


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


def list_available_quizzes(id: int, db: Session, current_student: CurrentUser):
    check_student(id, db, current_student)

    

    