import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    source_document_id = Column(String(36), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    is_competency_assessment = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), default="ready")  # draft, ready, archived
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User")
    source_document = relationship("Document", back_populates="quizzes")
    competency = relationship("Competency")
    questions = relationship("QuizQuestion", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    options_json = Column(JSON, nullable=False)  # Exactly 4 options: ["A", "B", "C", "D"]
    correct_option = Column(Integer, nullable=False)  # 0, 1, 2, or 3
    explanation = Column(Text, nullable=False)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    difficulty = Column(String(50), default="medium")  # easy, medium, hard
    source_ref = Column(String(255), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    competency = relationship("Competency")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    quiz_id = Column(String(36), ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)  # Percentage score (0-100)
    answers_json = Column(JSON, nullable=True)  # {question_id: selected_option}
    completed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User", back_populates="quiz_attempts")
