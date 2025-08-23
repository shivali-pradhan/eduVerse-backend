from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.course_models import Course, Module, Enrollment
from models.quiz_models import Quiz, Question, Option, QuizAttempt, QuizResult
from schemas.request_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuizAttemptCreate, QuestionUpdate
from schemas.token_schemas import CurrentUser
from .course import check_instructor_course


def check_module(id: int, db: Session, current_instructor: CurrentUser):
    module = db.query(Module).filter(Module.id == id).first()
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {id}")
    check_instructor_course(module.course_id, db, current_instructor)
    return module


def create_quiz(request: QuizCreate, db: Session, current_instructor: CurrentUser):
    check_module(request.module_id, db, current_instructor)
    
    new_quiz = Quiz(
        title = request.title,
        duration = request.duration,
        marks_per_ques = request.marks_per_ques,
        total_marks = 0,
        module_id = request.module_id
    )
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)

    return new_quiz


def update_quiz(id: int, request: QuizUpdate, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {id}")
    
    check_module(quiz.module_id, db, current_instructor)
    
    quiz.title = request.title
    quiz.duration = request.duration
    quiz.points = request.points

    db.commit()
    db.refresh(quiz)

    return quiz


def delete_quiz(id: int, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {id}")
    check_module(quiz.module_id, db, current_instructor)

    db.delete(quiz)
    db.commit()

    return None


def add_question(id: int, request: QuestionCreate, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {id}")
    check_module(quiz.module_id, db, current_instructor)

    new_question = Question(
        text = request.text,
        quiz_id = id
    )
    db.add(new_question)
    db.flush()
    quiz.total_marks += quiz.marks_per_ques

    options_list = []

    for opt in request.options:
        new_option = Option(
            value = opt.value,
            question_id = new_question.id
        )
        db.add(new_option)
        db.flush()
        options_list.append(opt)

    corr_opt_idx = request.correct_option_index
    if corr_opt_idx <= 0 or corr_opt_idx > len(options_list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid correct option index")
    
    new_question.correct_option_id = corr_opt_idx

    db.commit()
    db.refresh(new_question)

    return new_question


def update_question(quiz_id: int, question_id: int, request: QuestionUpdate, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    check_module(quiz.module_id, db, current_instructor)

    question = db.query(Question).filter(Question.id == question_id, Question.quiz_id == quiz_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    
    question.text = request.text

    options = db.query(Option).filter(Option.question_id == question.id)
    options.delete()

    for opt in request.options:
        new_option = Option(
            value = opt.value,
            question_id = question.id
        )
        db.add(new_option)

    db.commit()
    db.refresh(question)

    return question


def delete_question(quiz_id: int, question_id: int, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    check_module(quiz.module_id, db, current_instructor)

    question = db.query(Question).filter(Question.id == question_id, Question.quiz_id == quiz_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")

    db.delete(question)
    quiz.total_marks -= quiz.marks_per_ques
    db.commit()

    return None


def attempt_quiz(quiz_id: int, request: QuizAttemptCreate, db: Session, current_student: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    
    module = db.query(Module).filter(Module.id == quiz.module_id).first()
    if not module:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {quiz.module_id}")
    
    course = db.query(Course).filter(Course.id == module.course_id).first()
    if not course:     
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No module with id: {module.course_id}")
    
    course_enrollment = db.query(Enrollment).filter(Enrollment.student_id == current_student.id, Enrollment.course_id == course.id).first()
    if not course_enrollment:     
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    
    attempts = []
    score = 0

    for attempt in request.question_answers:

        question = db.query(Question).filter(Question.id == attempt.question_id, Question.quiz_id == quiz_id).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid question")
        
        option = db.query(Option).filter(Option.id == attempt.option_id, Option.question_id == question.id)
        if not option:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid option")
        
        if question.correct_option_id == attempt.option_id:
            score += 1

        new_quiz_attempt = QuizAttempt(
            student_id = current_student.id,
            quiz_id = quiz_id,
            question_id = attempt.question_id,
            answer = attempt.option_id
        )
        db.add(new_quiz_attempt)
        db.flush()
        
        attempts.append({ "question_id": attempt.question_id, "answer": attempt.option_id})

    quiz_result = QuizResult(
        student_id = current_student.id,
        quiz_id = quiz_id,
        score = score * quiz.marks_per_ques
    )
    db.add(quiz_result)
    db.commit()
    db.refresh(new_quiz_attempt)
    db.refresh(quiz_result)

    return { "attempts": attempts, "score": score }
    

def get_my_attempts(quiz_id: int, db: Session, current_student: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    
    quiz_attempts = db.query(QuizAttempt.question_id, QuizAttempt.answer, Question.correct_option_id).join(
        Question, Question.id == QuizAttempt.question_id).filter(
        QuizAttempt.student_id == current_student.id,
        QuizAttempt.quiz_id == quiz_id).all()
    if not quiz_attempts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not attempted")
        
    return quiz_attempts
  

def get_all_attempts(quiz_id: int, db: Session, current_instructor: CurrentUser):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No quiz with id: {quiz_id}")
    
    check_module(quiz.module_id, db, current_instructor)
    quiz_attempts = db.query(QuizAttempt).join(
        Question, Question.id == QuizAttempt.question_id
        ).filter(QuizAttempt.quiz_id == quiz_id).all()
    
    if not quiz_attempts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not attempted")

    return quiz_attempts