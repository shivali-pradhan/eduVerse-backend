from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from .base_model import MyBaseModel
from database import Base

class User(MyBaseModel):
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    role = Column(String, nullable=False)

    student_profile = relationship("Student", back_populates="user")
    instructor_profile = relationship("Instructor", back_populates="user")


class BaseUser(Base):  
    __abstract__ = True

    id = Column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, nullable=False)


class Student(BaseUser):
    __tablename__ = "students"

    user = relationship("User", back_populates="student_profile")
    enrollments = relationship("Enrollment", back_populates="student")
    enrolled_in = relationship("Course", secondary="enrollments", back_populates="students_enrolled")
    quiz_attempts = relationship("QuizAttempt", back_populates="student")
    quiz_results = relationship("QuizResult", back_populates="student")

class Instructor(BaseUser):
    __tablename__ = "instructors"

    qualification = Column(String)

    user = relationship("User", back_populates="instructor_profile")
    courses = relationship("Course", back_populates="creator")