from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.competency import CompetencyResponse


class AssessmentQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    assessment_id: str
    competency_id: str
    competency: Optional[CompetencyResponse] = None
    question_type: str
    difficulty: str
    prompt: str
    options_json: List[str]
    source_ref: Optional[str] = None


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: str
    title: str
    framework_id: str
    status: str
    metadata_json: Optional[Dict[str, Any]] = None
    questions: Optional[List[AssessmentQuestionResponse]] = None



class CreateAttemptRequest(BaseModel):
    pass


class AttemptAnswerRequest(BaseModel):
    question_id: str
    selected_answer: int  # option index
    response_time_ms: Optional[int] = None


class AttemptAnswerResponse(BaseModel):
    id: str
    attempt_id: str
    question_id: str
    selected_answer: Any
    is_correct: bool


class AttemptResultResponse(BaseModel):
    attempt_id: str
    assessment_id: str
    score: float
    total_questions: int
    correct_answers: int
    competency_breakdown: Dict[str, Dict[str, Any]]
    completed_at: Optional[datetime] = None
