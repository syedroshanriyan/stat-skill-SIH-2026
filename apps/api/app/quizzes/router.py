from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.models.competency import Competency
from app.schemas.quiz import (
    GenerateQuizRequest,
    QuizResponse,
    QuizQuestionResponse,
    StartQuizAttemptResponse,
    SubmitQuizAttemptRequest,
    QuizAttemptResultResponse,
)
from app.quizzes.service import generate_quiz_from_document, score_quiz_submission

router = APIRouter(tags=["Quizzes"])


@router.post("/quizzes/generate", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def generate_quiz(
    payload: GenerateQuizRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        quiz = generate_quiz_from_document(
            db=db,
            owner_id=current_user.id,
            document_id=payload.source_document_id,
            competency_id=payload.competency_id,
            difficulty=payload.difficulty,
            question_count=payload.question_count,
            title=payload.title,
            is_competency_assessment=payload.is_competency_assessment
        )
        return quiz
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/quizzes", response_model=List[QuizResponse])
def list_my_quizzes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quizzes = db.query(Quiz).filter(Quiz.owner_id == current_user.id).order_by(Quiz.created_at.desc()).all()
    return quizzes


@router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.owner_id == current_user.id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return quiz


@router.post("/quizzes/{quiz_id}/attempts", response_model=StartQuizAttemptResponse, status_code=status.HTTP_201_CREATED)
def start_quiz_attempt(
    quiz_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")

    attempt = QuizAttempt(
        quiz_id=quiz.id,
        user_id=current_user.id,
        score=0.0
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    questions = db.query(QuizQuestion).filter(QuizQuestion.quiz_id == quiz.id).all()
    q_responses = [
        QuizQuestionResponse(
            id=q.id,
            quiz_id=q.quiz_id,
            prompt=q.prompt,
            options_json=q.options_json,
            competency_id=q.competency_id,
            difficulty=q.difficulty,
            source_ref=q.source_ref
        )
        for q in questions
    ]

    return StartQuizAttemptResponse(
        attempt_id=attempt.id,
        quiz_id=quiz.id,
        title=quiz.title,
        questions=q_responses
    )


@router.post("/quiz-attempts/{attempt_id}/submit", response_model=QuizAttemptResultResponse)
def submit_quiz_attempt(
    attempt_id: str,
    payload: SubmitQuizAttemptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = score_quiz_submission(
            db=db,
            attempt_id=attempt_id,
            user_id=current_user.id,
            answers=payload.answers
        )
        return QuizAttemptResultResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
