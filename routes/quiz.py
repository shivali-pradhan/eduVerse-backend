from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.request_schemas import QuizCreate, QuestionCreate, QuizAttemptCreate, QuestionUpdate
from schemas.response_schemas import QuizBase, InstructorQuestionResponse, StudentQuizAttemptResponse, InstructorQuizAttemptResponse
from schemas.token_schemas import CurrentUser
from repositories import quiz
from auth.dependencies import require_instructor, require_student, get_current_user
from database import get_db

router = APIRouter(
    prefix = "/quizzes",
    tags = ["quizzes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=QuizBase)
def create_quiz(request: QuizCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.create_quiz(request, db, current_user)

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=QuizBase)
def update_quiz(id: int, request: QuizCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.update_quiz(id, request, db, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.delete_quiz(id, db, current_user)

@router.post("/{id}/questions", status_code=status.HTTP_201_CREATED, response_model=InstructorQuestionResponse)
def add_question(id: int, request: QuestionCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.add_question(id, request, db, current_user)

@router.put("/{quiz_id}/questions/{ques_id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructorQuestionResponse)
def update_question(quiz_id: int, ques_id: int, request: QuestionUpdate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.update_question(quiz_id, ques_id, request, db, current_user)

@router.post("/{quiz_id}/questions/{ques_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(quiz_id: int, ques_id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.delete_question(quiz_id, ques_id, db, current_user)

''' Attempts '''

@router.post("/{id}/attempts", status_code=status.HTTP_201_CREATED)
def attempt_quiz(id: int, request: QuizAttemptCreate, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return quiz.attempt_quiz(id, request, db, current_user)

@router.get("/{id}/my_attempts", response_model=List[StudentQuizAttemptResponse])
def get_my_attempts(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_student)):
    return quiz.get_my_attempts(id, db, current_user)

@router.get("/{id}/all_attempts", response_model=List[InstructorQuizAttemptResponse])
def get_all_attempts(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(require_instructor)):
    return quiz.get_all_attempts(id, db, current_user)