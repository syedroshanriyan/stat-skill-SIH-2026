import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class CompetencyFramework(Base):
    __tablename__ = "competency_frameworks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    track_id = Column(String(36), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    version = Column(String(50), nullable=False, default="1.0.0")
    status = Column(String(50), default="active")

    track = relationship("Track", back_populates="frameworks")
    competencies = relationship("Competency", back_populates="framework")
    assessments = relationship("Assessment", back_populates="framework")


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    framework_id = Column(String(36), ForeignKey("competency_frameworks.id", ondelete="CASCADE"), nullable=False, index=True)
    parent_id = Column(String(36), ForeignKey("competencies.id", ondelete="SET NULL"), nullable=True)
    code = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # Statistical, Technical, Digital Governance, Behavioural/Managerial
    description = Column(Text, nullable=False)
    level_definitions_json = Column(JSON, nullable=True)  # { "1": "Novice", "2": "Beginner", ... }

    framework = relationship("CompetencyFramework", back_populates="competencies")
    parent = relationship("Competency", remote_side=[id], backref="children")
    role_competencies = relationship("RoleCompetency", back_populates="competency")
    user_competencies = relationship("UserCompetency", back_populates="competency")
    skill_gaps = relationship("SkillGap", back_populates="competency")
    resource_mappings = relationship("ResourceCompetency", back_populates="competency")
    assessment_questions = relationship("AssessmentQuestion", back_populates="competency")


class RoleCompetency(Base):
    __tablename__ = "role_competencies"

    role_id = Column(String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), primary_key=True)
    required_level = Column(Integer, nullable=False, default=3)  # 1 to 5
    weight = Column(Float, nullable=False, default=1.0)
    priority = Column(String(50), nullable=False, default="MEDIUM")  # CRITICAL, HIGH, MEDIUM, LOW

    role = relationship("Role", back_populates="role_competencies")
    competency = relationship("Competency", back_populates="role_competencies")


class UserCompetency(Base):
    __tablename__ = "user_competencies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Float, nullable=False, default=0.0)  # 0 to 100
    proficiency_level = Column(Integer, nullable=False, default=1)  # 1 to 5
    confidence = Column(Float, nullable=False, default=0.5)  # 0.0 to 1.0
    source = Column(String(100), nullable=False, default="diagnostic")  # diagnostic, quiz, evidence, assessment
    assessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    version = Column(Integer, default=1)

    user = relationship("User", back_populates="competencies")
    competency = relationship("Competency", back_populates="user_competencies")
    evidence_items = relationship("CompetencyEvidence", back_populates="user_competency")


class CompetencyEvidence(Base):
    __tablename__ = "competency_evidence"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False)
    user_competency_id = Column(String(36), ForeignKey("user_competencies.id", ondelete="CASCADE"), nullable=True)
    evidence_type = Column(String(50), nullable=False)  # project, certificate, assessment, quiz
    evidence_id = Column(String(36), nullable=False)
    contribution = Column(Float, default=10.0)  # score points contributed
    verified_status = Column(String(50), default="unverified")  # unverified, verified, rejected

    user_competency = relationship("UserCompetency", back_populates="evidence_items")
