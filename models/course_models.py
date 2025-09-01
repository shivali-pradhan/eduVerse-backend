from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base
from .base_model import MyBaseModel



class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "course_id"),
    )

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")


class Course(MyBaseModel):
    __tablename__ = "courses"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    credits = Column(Integer)
    duration = Column(Integer)

    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="SET NULL"))
    
    creator = relationship("Instructor", back_populates="courses")
    modules = relationship("Module", back_populates="parent_course", passive_deletes=True)
    enrollments = relationship("Enrollment", back_populates="course", passive_deletes=True)
    students_enrolled = relationship("Student", secondary="enrollments", back_populates="enrolled_in")


class Module(MyBaseModel):
    __tablename__ = "modules"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    duration = Column(Integer)

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)

    parent_course = relationship("Course", back_populates="modules")
    content_files = relationship("LearningContentFile", back_populates="module", passive_deletes=True)
    quizzes = relationship("Quiz", back_populates="module", passive_deletes=True)


class LearningContentFile(MyBaseModel):
    __tablename__ = "learning_content_files"

    file_name = Column(String)
    file_url = Column(String)
    file_type = Column(String)

    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    
    module = relationship("Module", back_populates="content_files")
