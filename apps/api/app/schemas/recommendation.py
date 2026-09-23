from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.competency import CompetencyResponse


class LearningResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    provider_type: str  # igot, nssta, industry, academia
    provider_external_id: str
    title: str
    description: str
    url: str
    level: str
    duration: str
    is_demo: bool
    visibility: str = "PUBLIC"
    track_code: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    resource_id: str
    resource: LearningResourceResponse
    competency_id: str
    competency: CompetencyResponse
    rank: int
    score: float
    explanation: str
    status: str  # suggested, saved, started, completed, dismissed
    generated_at: datetime

