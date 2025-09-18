from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database
from routes import student, instructor, course, module, quiz
from auth import routes as auth_route

from models import *    

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in cross-origin requests
)

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