from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.competency import CompetencyResponse


class SkillGapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    competency_id: str
    competency: CompetencyResponse
    required_level: int
    current_score: float
    gap_value: float
    priority: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str    # OPEN, IN_PROGRESS, RESOLVED
    explanation: Optional[str] = None
    created_at: datetime
    updated_at: datetime

