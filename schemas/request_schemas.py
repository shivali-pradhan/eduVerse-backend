from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    password: str
    email: str
    

class StudentCreate(UserCreate):
    pass

class InstructorCreate(UserCreate):
    pass



class CourseCreate(BaseModel):
    name: str
    description: Optional[str]
    credits: int

class ModuleCreate(BaseModel):
    name: str
    description: Optional[str]


class QuizCreate(BaseModel):
    title: str
    duration: int
    points: Optional[int]

class OptionCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    options: List[OptionCreate]
    correct_option_index: int

class QuestionAttempt(BaseModel):
    question_id: int
    option_id: int

class QuizAttempt(BaseModel):
    question_answers: List[QuestionAttempt]

