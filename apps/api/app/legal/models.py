import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class LegalStatute(Base):
    __tablename__ = "legal_statutes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False, index=True)
    short_title = Column(String(100), nullable=False, index=True)
    act_number = Column(String(100), nullable=False)
    jurisdiction = Column(String(100), nullable=False, default="Republic of India")
    publisher = Column(String(255), nullable=False)
    source_url = Column(String(500), nullable=False)
    canonical_url = Column(String(500), nullable=False)
    enactment_date = Column(DateTime, nullable=False)
    commencement_date = Column(DateTime, nullable=False)
    amendment_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=False)
    retrieval_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)
    version = Column(String(50), nullable=False, default="1.0")
    status = Column(String(50), nullable=False, default="active", index=True)  # active, amended, repealed, superseded
    superseded_by = Column(String(36), ForeignKey("legal_statutes.id", ondelete="SET NULL"), nullable=True)
    language = Column(String(20), nullable=False, default="en")
    document_type = Column(String(50), nullable=False, default="Act")  # Act, Rule, Regulation, Notification
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    sections = relationship("LegalSection", back_populates="statute", cascade="all, delete-orphan")


class LegalSection(Base):
    __tablename__ = "legal_sections"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    statute_id = Column(String(36), ForeignKey("legal_statutes.id", ondelete="CASCADE"), nullable=False, index=True)
    section_number = Column(String(50), nullable=False, index=True)
    section_title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    citation_tag = Column(String(100), nullable=False, index=True)
    effective_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="active")

    statute = relationship("LegalStatute", back_populates="sections")


class LegalClarificationSession(Base):
    __tablename__ = "legal_clarification_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=False, index=True)
    conversation_id = Column(String(100), nullable=False, index=True)
    query_history = Column(JSON, nullable=False, default=list)
    current_round = Column(Integer, default=1)
    max_rounds = Column(Integer, default=3)
    detected_intent = Column(String(50), nullable=True)
    detected_jurisdiction = Column(String(100), nullable=True)
    detected_act = Column(String(255), nullable=True)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
