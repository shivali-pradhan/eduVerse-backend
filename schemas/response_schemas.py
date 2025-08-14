from pydantic import BaseModel
from typing import List
import datetime


class UserBase(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    registered_at: datetime.datetime
    
    class Config:
        orm_mode = True


class StudentBase(UserBase):

    class Config:
        orm_mode = True


class InstructorBase(UserBase):

    class Config:
        orm_mode = True


class CourseBase(BaseModel):
    id: int
    name: str
    description: str
    credits: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class ModuleBase(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime.datetime
    
    class Config:
        orm_mode = True

class QuizBase(BaseModel):
    id: int
    title: str
    duration: int
    points: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True
   
class ModuleResponse(ModuleBase):
    quizzes: List[QuizBase]

    class Config:
        orm_mode = True

class CourseResponse(CourseBase):

    modules: List[ModuleBase] = []
    creator: InstructorBase
    students: List[StudentBase] = []

    class Config:
        orm_mode = True


class InstructorCourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    students: List[StudentBase] = []

    class Config:
        orm_mode = True

class StudentCourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    creator: InstructorBase

    class Config:
        orm_mode = True

class StudentResponse(StudentBase):
    enrolled_in: List[CourseResponse] = []

    class Config:
        orm_mode = True

class InstructorResponse(InstructorBase):
    courses: List[CourseBase] = []

    class Config:
        orm_mode = True



