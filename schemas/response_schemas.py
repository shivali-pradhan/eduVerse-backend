from pydantic import BaseModel
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
    duration: int
    credits: int
    created_at: datetime.datetime


class ModuleBase(MyBaseModel):
    id: int
    name: str
    description: str
    duration: int
    created_at: datetime.datetime

class QuizBase(MyBaseModel):
    id: int
    title: str
    duration: int
    marks_per_ques: int
    total_marks: int
    created_at: datetime.datetime

''' Response Schemas '''

class OptionResponse(MyBaseModel):
    id: int
    value: str

class StudentQuestionResponse(MyBaseModel):
    id: int
    text: str
    options: List[OptionResponse]

class InstructorQuestionResponse(StudentQuestionResponse):
    correct_option: OptionResponse

class StudentQuizResponse(QuizBase):
    questions: List[StudentQuestionResponse]

class InstructorQuizResponse(StudentQuizResponse):
    questions: List[InstructorQuestionResponse]

class StudentQuizScoreResponse(MyBaseModel):
    quiz_id: int
    score: int

class InstructorQuizScoreResponse(StudentQuizScoreResponse):
    student_id: int

class StudentQuizAttemptResponse(MyBaseModel):
    question_id: int
    answer: int
    correct_option_id: int

class InstructorQuizAttemptResponse(StudentQuizAttemptResponse):
    student_id: int

class ContentFileResponse(MyBaseModel):
    id: int
    file_name: str
    file_type: str
    file_url: str

class ModuleResponse(ModuleBase):
    content_files: List[ContentFileResponse]
    quizzes: List[StudentQuizResponse]

class Enrollment(MyBaseModel):
    enrolled_at: datetime.datetime

class CourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    creator: InstructorBase
    students_enrolled: List[StudentBase] = []


class InstructorCourseResponse(CourseBase):
    modules: List[ModuleBase] = []
    students_enrolled: List[StudentBase] = []


class StudentCourseResponse(CourseBase):
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



