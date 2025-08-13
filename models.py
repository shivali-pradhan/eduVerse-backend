from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database import Base


class MyBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)


class BaseUser(MyBaseModel):
    
    __abstract__ = True

    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    role = Column(String)
    registered_at = Column(DateTime)


class Student(BaseUser):
    __tablename__ = "students"

    enrolled_in = relationship("Enrollment", back_populates="student")


class Instructor(BaseUser):
    __tablename__ = "instructors"

    courses = relationship("Course", back_populates="creator")


class Course(MyBaseModel):
    __tablename__ = "courses"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    credits = Column(Integer)
    created_at = Column(DateTime)

    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="SET NULL"))
    
    creator = relationship("Instructor", back_populates="courses")
    modules = relationship("Module", back_populates="parent_course")
    students_enrolled = relationship("Enrollment", back_populates="course")


class Enrollment(Base):
    __tablename__ = "enrollments"
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "course_id"),
    )

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="SET NULL"))
    enrolled_at = Column(DateTime)

    student = relationship("Student", back_populates="enrolled_in")
    course = relationship("Course", back_populates="students_enrolled")


class Module(MyBaseModel):
    __tablename__ = "modules"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime)

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    
    parent_course = relationship("Course", back_populates="modules")
    learning_content = relationship("LearningContent", back_populates="module")


class LearningContent(MyBaseModel):
    __tablename__ = "learning_content"

    # text = Column(String(255))
    # video_link = Column(String(200))
    
    created_at = Column(DateTime)
    
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    
    module = relationship("Module", back_populates="learning_content")







