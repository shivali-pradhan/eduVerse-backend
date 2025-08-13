from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models import Student, Enrollment, Course
from my_schemas.request_schemas import StudentCreate
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
    