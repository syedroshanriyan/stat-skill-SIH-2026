import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    provider_type = Column(String(50), nullable=False, index=True)  # igot, nssta, industry, academia
    provider_external_id = Column(String(100), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(500), nullable=False)
    level = Column(String(50), default="Intermediate")
    duration = Column(String(100), default="4 weeks")
    is_demo = Column(Boolean, default=False)
    visibility = Column(String(50), default="PUBLIC", nullable=False, index=True)  # PUBLIC, TRACK, ORGANIZATION, PRIVATE
    track_code = Column(String(50), nullable=True, index=True)  # GOVERNMENT, INDUSTRY, ACADEMIA
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True, index=True)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    metadata_json = Column(JSON, nullable=True)

    resource_competencies = relationship("ResourceCompetency", back_populates="resource")
    recommendations = relationship("Recommendation", back_populates="resource")
    learning_path_items = relationship("LearningPathItem", back_populates="resource")


class ResourceCompetency(Base):
    __tablename__ = "resource_competencies"

    resource_id = Column(String(36), ForeignKey("learning_resources.id", ondelete="CASCADE"), primary_key=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), primary_key=True)
    relevance_score = Column(Float, nullable=False, default=1.0)  # 0.0 to 1.0

    resource = relationship("LearningResource", back_populates="resource_competencies")
    competency = relationship("Competency", back_populates="resource_mappings")


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resource_id = Column(String(36), ForeignKey("learning_resources.id", ondelete="CASCADE"), nullable=False, index=True)
    competency_id = Column(String(36), ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False, index=True)
    rank = Column(Integer, nullable=False, default=1)
    score = Column(Float, nullable=False, default=0.0)
    explanation = Column(Text, nullable=False)
    status = Column(String(50), default="suggested")  # suggested, saved, started, completed, dismissed
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="recommendations")
    resource = relationship("LearningResource", back_populates="recommendations")
    competency = relationship("Competency")
