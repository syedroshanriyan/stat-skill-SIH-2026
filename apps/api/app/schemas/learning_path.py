from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.recommendation import LearningResourceResponse
from app.schemas.competency import CompetencyResponse


class LearningPathItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    learning_path_id: str
    resource_id: str
    resource: Optional[LearningResourceResponse] = None
    competency_id: str
    competency: Optional[CompetencyResponse] = None
    sequence: int
    status: str  # pending, in_progress, completed, skipped


class LearningPathResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    goal: str
    status: str  # active, completed, archived
    items: List[LearningPathItemResponse] = []
    created_at: datetime



class CreateLearningPathRequest(BaseModel):
    title: str
    goal: str
    resource_ids: List[str] = []


class UpdateLearningPathItemRequest(BaseModel):
    status: str  # pending, in_progress, completed, skipped
