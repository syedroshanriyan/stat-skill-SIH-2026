from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CompetencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    framework_id: str
    parent_id: Optional[str] = None
    code: str
    name: str
    category: str
    description: str
    level_definitions_json: Optional[Dict[str, str]] = None


class FrameworkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    track_id: str
    name: str
    version: str
    status: str
    competencies_count: Optional[int] = 0


class UserCompetencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    competency_id: str
    competency: CompetencyResponse
    score: float
    proficiency_level: int
    confidence: float
    source: str
    assessed_at: datetime
    version: int


class RoleCompetencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_id: str
    competency_id: str
    competency: CompetencyResponse
    required_level: int
    weight: float
    priority: str


class CompetencyHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    competency_id: str
    competency: Optional[CompetencyResponse] = None
    assessment_attempt_id: Optional[str] = None
    quiz_attempt_id: Optional[str] = None
    score_before: float
    score_after: float
    delta: float
    confidence_before: float
    confidence_after: float
    source: str
    timestamp: datetime


