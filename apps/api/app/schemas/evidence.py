from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CreateEvidenceRequest(BaseModel):
    type: str  # project, github, certificate, internship
    title: str
    description: str
    url: Optional[str] = None
    storage_key: Optional[str] = None


class UpdateEvidenceRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None  # submitted, ai_analyzed, pending_verification, verified, rejected


class EvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    type: str
    title: str
    description: str
    url: Optional[str] = None
    storage_key: Optional[str] = None
    status: str
    ai_analysis_json: Optional[Dict[str, Any]] = None
    created_at: datetime

