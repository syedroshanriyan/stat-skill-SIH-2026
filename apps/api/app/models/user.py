import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    code = Column(String(50), unique=True, nullable=False, index=True)  # GOVERNMENT, INDUSTRY, ACADEMIA
    name = Column(String(100), nullable=False)

    profiles = relationship("Profile", back_populates="track")
    roles = relationship("Role", back_populates="track")
    frameworks = relationship("CompetencyFramework", back_populates="track")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False, index=True)
    type = Column(String(50), nullable=False)  # GOVERNMENT, INDUSTRY, ACADEMIA
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    memberships = relationship("Membership", back_populates="organization")
    roles = relationship("Role", back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(150), nullable=False)
    auth_provider_id = Column(String(100), nullable=True)
    status = Column(String(50), default="active")  # active, inactive, suspended
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    profile = relationship("Profile", back_populates="user", uselist=False)
    memberships = relationship("Membership", back_populates="user")
    competencies = relationship("UserCompetency", back_populates="user")
    skill_gaps = relationship("SkillGap", back_populates="user")
    recommendations = relationship("Recommendation", back_populates="user")
    learning_paths = relationship("LearningPath", back_populates="user")
    assessment_attempts = relationship("AssessmentAttempt", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    documents = relationship("Document", back_populates="user")
    evidence_records = relationship("Evidence", back_populates="user")


class Membership(Base):
    __tablename__ = "memberships"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # learner, official, student, professional, org_admin, institution_admin, platform_admin
    status = Column(String(50), default="active")

    user = relationship("User", back_populates="memberships")
    organization = relationship("Organization", back_populates="memberships")


class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    track_id = Column(String(36), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)

    track = relationship("Track", back_populates="roles")
    organization = relationship("Organization", back_populates="roles")
    role_competencies = relationship("RoleCompetency", back_populates="role")
    profiles = relationship("Profile", back_populates="target_role")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    track_id = Column(String(36), ForeignKey("tracks.id"), nullable=False, index=True)
    designation = Column(String(150), nullable=True)
    department = Column(String(150), nullable=True)
    education_json = Column(JSON, nullable=True)
    experience_json = Column(JSON, nullable=True)
    career_goal = Column(String(255), nullable=True)
    target_role_id = Column(String(36), ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    metadata_json = Column(JSON, nullable=True)

    user = relationship("User", back_populates="profile")
    track = relationship("Track", back_populates="profiles")
    target_role = relationship("Role", back_populates="profiles")
