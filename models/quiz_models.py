from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from database import Base
from .base_model import MyBaseModel



class Quiz(MyBaseModel):
    __tablename__ = "quizzes"

    title = Column(String(100))
    duration = Column(Integer)
    marks_per_ques = Column(Integer, default=1)
    total_marks = Column(Integer)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))

    module = relationship("Module", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    results = relationship("QuizResult", back_populates="quiz")

class Question(MyBaseModel):
    __tablename__ = "questions"

    text = Column(String(100))
    correct_option_id = Column(Integer, ForeignKey("options.id", ondelete="SET NULL"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", foreign_keys="Option.question_id")
    correct_option = relationship("Option", foreign_keys=[correct_option_id])
    attempts = relationship("QuizAttempt", back_populates="question")


class Option(MyBaseModel):
    __tablename__ = "options"

    value = Column(String(100))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))

    question = relationship("Question", back_populates="options", foreign_keys=[question_id])


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "quiz_id", "question_id"),
    )

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="SET NULL"))
    answer = Column(Integer, ForeignKey("options.id", ondelete="SET NULL"))

    student = relationship("Student", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")


class QuizResult(Base):
    __tablename__ = "quiz_results"  
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "quiz_id"),
    )

    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="SET NULL"))
    score = Column(Integer)

    student = relationship("Student", back_populates="quiz_results")
    quiz = relationship("Quiz", back_populates="results")