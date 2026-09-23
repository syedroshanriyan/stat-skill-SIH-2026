import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    framework_id = Column(String(36), ForeignKey("competency_frameworks.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False, default="DIAGNOSTIC")  # DIAGNOSTIC, BENCHMARK, COURSE
    title = Column(String(200), nullable=False)
    status = Column(String(50), default="active")  # active, archived
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    framework = relationship("CompetencyFramework", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment")
    attempts = relationship("AssessmentAttempt", back_populates="assessment")


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    question_type = Column(String(50), default="MCQ")  # MCQ, SCENARIO
    difficulty = Column(String(50), default="medium")  # easy, medium, hard
    prompt = Column(Text, nullable=False)
    options_json = Column(JSON, nullable=False)  # List of strings: ["Option A", "Option B", ...]
    answer_json = Column(JSON, nullable=False)   # Correct index: 0 or answer payload
    source_ref = Column(String(255), nullable=True)

    assessment = relationship("Assessment", back_populates="questions")
    competency = relationship("Competency", back_populates="assessment_questions")
    answers = relationship("AttemptAnswer", back_populates="question")


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    assessment_id = Column(String(36), ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime, nullable=True)

    assessment = relationship("Assessment", back_populates="attempts")
    user = relationship("User", back_populates="assessment_attempts")
    answers = relationship("AttemptAnswer", back_populates="attempt")


class AttemptAnswer(Base):
    __tablename__ = "attempt_answers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    attempt_id = Column(String(36), ForeignKey("assessment_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=True)

    attempt = relationship("AssessmentAttempt", back_populates="answers")
    question = relationship("AssessmentQuestion", back_populates="answers")
