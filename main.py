from fastapi import FastAPI

import database
from routes import student, instructor, course

from models import *    

app = FastAPI()

database.create_db_tables()

app.include_router(student.router)
app.include_router(instructor.router)
app.include_router(course.router)



@app.get("/")
def home():
    return "Home Page"