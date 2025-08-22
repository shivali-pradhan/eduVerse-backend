from fastapi import FastAPI
from fastapi_pagination import add_pagination, set_params

from schemas.custom_pagination import CustomParams
import database
from routes import student, instructor, course, module, quiz
from auth import routes as auth_route

from models import *    

app = FastAPI()

set_params(CustomParams)
add_pagination(app)
database.create_db_tables()

app.include_router(auth_route.router)
app.include_router(student.router)
app.include_router(instructor.router)
app.include_router(course.router)
app.include_router(module.router)
app.include_router(quiz.router)


@app.get("/")
def root():
    return "Home Page"