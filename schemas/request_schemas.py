from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional, List
import string

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=30)
    password: str
    # confirm_password: str

    @field_validator("password")
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in string.punctuation for c in value):
            raise ValueError("Password must contain at least one special character")
        return value
    
    # @model_validator(mode="after")
    # def match_passwords(self) -> str:
    #     if self.password != self.confirm_password:
    #         raise ValueError("Passwords do not match")
    #     return self
  

class StudentCreate(UserCreate):
    pass

class InstructorCreate(UserCreate):
    qualification: Optional[str] = ""


class UserUpdate(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class StudentUpdate(UserUpdate):
    pass

class InstructorUpdate(UserUpdate):
    qualification: Optional[str] = ""

class CourseCreate(BaseModel):
    name: str
    description: Optional[str]
    credits: int = Field(..., ge=0)
    instructor_id: int

class CourseUpdate(BaseModel):
    name: str
    description: Optional[str]
    credits: int = Field(..., ge=0)

class ModuleCreate(BaseModel):
    name: str
    description: Optional[str]
    duration: int = Field(..., ge=0)
    course_id: int

class ModuleUpdate(BaseModel):
    name: str
    description: Optional[str]
    duration: int

class EnrollmentCreate(BaseModel):
    course_id: int

class QuizCreate(BaseModel):
    title: str
    duration: int = Field(..., ge=0)
    marks_per_ques: int = Field(..., ge=0)
    module_id: int

class QuizUpdate(BaseModel):
    title: str
    duration: int = Field(..., ge=0)
    marks_per_ques: int = Field(..., ge=0)

class OptionCreate(BaseModel):
    value: str

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

