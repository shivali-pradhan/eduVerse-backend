from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import datetime

from models.course_models import Module
from models.quiz_models import Quiz, Question, Option
from schemas.request_schemas import QuizCreate, QuestionCreate
from .course import check_instructor_course

def check_module(i_id: int, c_id: int, m_id: int, db: Session):
    
    check_instructor_course(i_id, c_id, db)
    module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {m_id} in course_id: {c_id}")

def list_quizzes(i_id: int, c_id: int, m_id: int, db: Session):
    check_instructor_course(i_id, c_id, db)
    module = db.query(Module).filter(Module.id == m_id, Module.course_id == c_id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No such module with id: {m_id} in course with id: {c_id}")
    
    quizzes = db.query(Quiz).filter(Quiz.module_id == m_id).all()

    return quizzes

def create_quiz(i_id: int, c_id: int, m_id: int, request: QuizCreate, db: Session):
    check_module(i_id, c_id, m_id, db)
    
    new_quiz = Quiz(
        title = request.title,
        duration = request.duration,
        points = request.points,
        created_at = datetime.datetime.now(),
        module_id = m_id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz


def update_quiz(i_id: int, c_id: int, m_id: int, q_id: int, request: QuizCreate, db: Session):
    check_module(i_id, c_id, m_id, db)
    
    quiz = db.query(Quiz).filter(Quiz.id == m_id, Quiz.module_id == m_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {q_id} in module_id: {m_id}")
    
    quiz.title = request.title
    quiz.duration = quiz.duration
    quiz.points = quiz.points

    db.commit()
    db.refresh(quiz)

    return quiz

def delete_quiz(i_id: int, c_id: int, m_id: int, q_id: int, db: Session):
    check_module(i_id, c_id, m_id, db)
    
    quiz = db.query(Quiz).filter(Quiz.id == m_id, Quiz.module_id == m_id)
    if not quiz.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {q_id} in module_id: {m_id}")
    
    quiz.delete(synchronize_session=False)
    db.commit()

    return "deleted"


def add_question(i_id: int, c_id: int, m_id: int, q_id: int, request: QuestionCreate, db: Session):
    check_module(i_id, c_id, m_id, db)
    
    quiz = db.query(Quiz).filter(Quiz.id == m_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {q_id} in module_id: {m_id}")
    
    new_question = Question(
        text = request.text,
        quiz_id = q_id
    )
    db.add(new_question)
    db.flush()

    options_list = []

    for opt in request.options:
        new_option = Option(
            text = opt.text,
            question_id = new_question.id
        )
        db.add(new_option)
        db.flush()
        options_list.append(opt)

    new_question.correct_option_id = request.correct_option_index

    db.commit()
    db.refresh(new_question)

    return new_question


def update_question():
    pass

def delete_question():
    pass
