from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
  

class StudentCreate(UserCreate):
    pass

class InstructorCreate(UserCreate):
    qualification: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str

class StudentUpdate(UserUpdate):
    pass

class InstructorUpdate(UserUpdate):
    qualification: str

class CourseCreate(BaseModel):
    name: str
    description: Optional[str]
    credits: int
    instructor_id: int

class CourseUpdate(BaseModel):
    name: str
    description: Optional[str]
    credits: int

class ModuleCreate(BaseModel):
    name: str
    description: Optional[str]
    course_id: int

class ModuleUpdate(BaseModel):
    name: str
    description: Optional[str]

class EnrollmentCreate(BaseModel):
    course_id: int

class QuizCreate(BaseModel):
    title: str
    duration: int
    points: Optional[int]
    module_id: int

class QuizUpdate(BaseModel):
    title: str
    duration: int
    points: Optional[int]

class OptionCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    options: List[OptionCreate]
    correct_option_index: int

class QuestionUpdate(BaseModel):
    text: str
    options: List[OptionCreate]
    correct_option_index: int

class QuestionAttemptCreate(BaseModel):
    question_id: int
    option_id: int

class QuizAttemptCreate(BaseModel):
    question_answers: List[QuestionAttemptCreate]

