import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text, JSON, Integer
from app.core.database import Base


def generate_uuid():
    return str(uuid.uuid4())


class ScrapedDocument(Base):
    __tablename__ = "scraped_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_domain = Column(String(100), nullable=False, index=True)
    source_url = Column(String(500), nullable=False, index=True)
    canonical_url = Column(String(500), nullable=False)
    publisher = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=False, default="Act")  # Act, Rule, Regulation, Handbook, Course
    publication_date = Column(DateTime, nullable=True)
    effective_date = Column(DateTime, nullable=True)
    retrieval_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    content_hash = Column(String(64), nullable=False, index=True)  # SHA-256
    version = Column(String(50), nullable=False, default="1.0")
    language = Column(String(20), nullable=False, default="en")
    jurisdiction = Column(String(100), nullable=False, default="India / Union")
    status = Column(String(50), nullable=False, default="active", index=True)  # active, parser_error, indexed, deprecated
    parser_error_message = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
