from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.schemas.competency import CompetencyResponse


class QuizQuestionModel(BaseModel):
    prompt: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    correct_option: int = Field(..., ge=0, le=3)
    explanation: str
    competency_code: Optional[str] = None
    difficulty: str = "medium"
    source_ref: str


class GenerateQuizRequest(BaseModel):
    source_document_id: str
    competency_id: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    question_count: int = Field(default=5, ge=1, le=20)
    title: Optional[str] = None
    is_competency_assessment: bool = True


class QuizQuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    quiz_id: str
    prompt: str
    options_json: List[str]
    explanation: Optional[str] = None
    competency_id: Optional[str] = None
    competency: Optional[CompetencyResponse] = None
    difficulty: str
    source_ref: str


class QuizResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    title: str
    source_document_id: Optional[str] = None
    competency_id: Optional[str] = None
    is_competency_assessment: bool = False
    status: str
    questions: Optional[List[QuizQuestionResponse]] = []
    created_at: datetime



class StartQuizAttemptResponse(BaseModel):
    attempt_id: str
    quiz_id: str
    title: str
    questions: List[QuizQuestionResponse]


class SubmitQuizAttemptRequest(BaseModel):
    answers: Dict[str, int]  # {question_id: selected_option_index}


class QuizAttemptResultResponse(BaseModel):
    attempt_id: str
    quiz_id: str
    score: float
    total_questions: int
    correct_answers: int
    competency_impact: Dict[str, Any]
    details: List[Dict[str, Any]]
    completed_at: datetime
