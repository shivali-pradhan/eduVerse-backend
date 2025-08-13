from pydantic import BaseModel
from typing import Optional

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