from pydantic import BaseModel, Field
from typing import List
import datetime

class MyBaseModel(BaseModel):

    class Config:
        orm_mode = True



class UserBase(MyBaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

class StudentBase(UserBase):
    pass


class InstructorBase(UserBase):
    qualification: str


class CourseBase(MyBaseModel):
    id: int
    name: str
    description: str
    credits: int
    created_at: datetime.datetime


class ModuleBase(MyBaseModel):
    id: int
    name: str
    description: str
    created_at: datetime.datetime


class QuizBase(MyBaseModel):
    id: int
    title: str
    duration: int
    points: int
    created_at: datetime.datetime


''' Response Schemas '''

class ModuleResponse(ModuleBase):
    quizzes: List[QuizBase]


class CourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    creator: InstructorBase
    students_enrolled: List[StudentBase] = []


class InstructorCourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    students_enrolled: List[StudentBase] = []


class StudentCourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    creator: InstructorBase


class StudentResponse(StudentBase):
    enrolled_in: List[CourseBase] = []


class InstructorResponse(InstructorBase):
    courses: List[CourseBase] = []

class OptionResponse(BaseModel):
    text: str

class QuestionResponse(BaseModel):
    text: str
    options: List[OptionResponse]



