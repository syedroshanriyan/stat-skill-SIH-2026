import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class CompetencyHistory(Base):
    __tablename__ = "competency_history"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_attempt_id = Column(String(36), nullable=True, index=True)
    quiz_attempt_id = Column(String(36), nullable=True, index=True)
    score_before = Column(Float, nullable=False)
    score_after = Column(Float, nullable=False)
    delta = Column(Float, nullable=False)
    confidence_before = Column(Float, nullable=False)
    confidence_after = Column(Float, nullable=False)
    source = Column(String(50), nullable=False, default="quiz")  # diagnostic, quiz, evidence
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = relationship("User")
    competency = relationship("Competency")
