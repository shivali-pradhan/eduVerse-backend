from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.request_schemas import QuizCreate, QuestionCreate
from schemas.response_schemas import ModuleBase
from repositories import quiz

from database import get_db

router = APIRouter(
    prefix = "/quizzes",
    tags = ["quizzes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_quiz(request: QuizCreate, db: Session = Depends(get_db)):
    return quiz.create_quiz(request, db)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_quiz(id: int, request: QuizCreate, db: Session = Depends(get_db)):
    return quiz.update_quiz(id, request, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int, db: Session = Depends(get_db)):
    return quiz.delete_quiz(id, db)

@router.post("/{id}/questions", status_code=status.HTTP_201_CREATED)
def add_question(id: int, request: QuestionCreate, db: Session = Depends(get_db)):
    return quiz.add_question(id, request, db)