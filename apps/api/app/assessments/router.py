from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User, Profile, Track
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AttemptAnswer
from app.models.competency import CompetencyFramework, Competency
from app.schemas.assessment import (
    AssessmentResponse,
    AssessmentQuestionResponse,
    CreateAttemptRequest,
    AttemptAnswerRequest,
    AttemptAnswerResponse,
    AttemptResultResponse,
)
from app.assessments.service import score_assessment_attempt

router = APIRouter(tags=["Assessments"])


@router.post("/assessments/diagnostic", response_model=AssessmentResponse)
def get_or_create_diagnostic(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    track_id = profile.track_id if profile else None

    if not track_id:
        track = db.query(Track).filter(Track.code == "GOVERNMENT").first()
        track_id = track.id if track else None

    # Find framework for track
    fw = db.query(CompetencyFramework).filter(CompetencyFramework.track_id == track_id).first()
    if not fw:
        fw = db.query(CompetencyFramework).first()

    # Find existing diagnostic assessment for framework
    assessment = db.query(Assessment).filter(
        Assessment.framework_id == fw.id,
        Assessment.type == "DIAGNOSTIC"
    ).first()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diagnostic assessment configured for your track"
        )

    # Return assessment with questions (without answer keys)
    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.assessment_id == assessment.id).all()
    q_responses = [
        AssessmentQuestionResponse(
            id=q.id,
            assessment_id=q.assessment_id,
            competency_id=q.competency_id,
            question_type=q.question_type,
            difficulty=q.difficulty,
            prompt=q.prompt,
            options_json=q.options_json,
            source_ref=q.source_ref
        )
        for q in questions
    ]

    return AssessmentResponse(
        id=assessment.id,
        type=assessment.type,
        title=assessment.title,
        framework_id=assessment.framework_id,
        status=assessment.status,
        metadata_json=assessment.metadata_json,
        questions=q_responses
    )


@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: str,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.assessment_id == assessment.id).all()
    q_responses = [
        AssessmentQuestionResponse(
            id=q.id,
            assessment_id=q.assessment_id,
            competency_id=q.competency_id,
            question_type=q.question_type,
            difficulty=q.difficulty,
            prompt=q.prompt,
            options_json=q.options_json,
            source_ref=q.source_ref
        )
        for q in questions
    ]

    return AssessmentResponse(
        id=assessment.id,
        type=assessment.type,
        title=assessment.title,
        framework_id=assessment.framework_id,
        status=assessment.status,
        metadata_json=assessment.metadata_json,
        questions=q_responses
    )


@router.post("/assessments/{assessment_id}/attempts", status_code=status.HTTP_201_CREATED)
def start_assessment_attempt(
    assessment_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    attempt = AssessmentAttempt(
        assessment_id=assessment.id,
        user_id=current_user.id,
        score=0.0,
        started_at=datetime.now(timezone.utc)
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {"attempt_id": attempt.id, "assessment_id": attempt.assessment_id, "started_at": attempt.started_at}


@router.post("/attempts/{attempt_id}/answers", response_model=AttemptAnswerResponse)
def record_attempt_answer(
    attempt_id: str,
    payload: AttemptAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.user_id == current_user.id
    ).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    question = db.query(AssessmentQuestion).filter(AssessmentQuestion.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    # Check if answer is correct
    try:
        is_correct = int(payload.selected_answer) == int(question.answer_json)
    except (ValueError, TypeError):
        is_correct = str(payload.selected_answer).strip() == str(question.answer_json).strip()

    # Upsert answer
    existing_ans = db.query(AttemptAnswer).filter(
        AttemptAnswer.attempt_id == attempt_id,
        AttemptAnswer.question_id == payload.question_id
    ).first()

    if existing_ans:
        existing_ans.selected_answer = payload.selected_answer
        existing_ans.is_correct = is_correct
        existing_ans.response_time_ms = payload.response_time_ms
        ans_record = existing_ans
    else:
        ans_record = AttemptAnswer(
            attempt_id=attempt_id,
            question_id=payload.question_id,
            selected_answer=payload.selected_answer,
            is_correct=is_correct,
            response_time_ms=payload.response_time_ms
        )
        db.add(ans_record)

    db.commit()
    db.refresh(ans_record)

    return AttemptAnswerResponse(
        id=ans_record.id,
        attempt_id=ans_record.attempt_id,
        question_id=ans_record.question_id,
        selected_answer=ans_record.selected_answer,
        is_correct=ans_record.is_correct
    )


@router.post("/attempts/{attempt_id}/complete", response_model=AttemptResultResponse)
def complete_attempt(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        result = score_assessment_attempt(db, attempt_id, current_user.id)
        return AttemptResultResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/attempts/{attempt_id}/result", response_model=AttemptResultResponse)
def get_attempt_result(
    attempt_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.user_id == current_user.id
    ).first()
    if not attempt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")

    questions = db.query(AssessmentQuestion).filter(AssessmentQuestion.assessment_id == attempt.assessment_id).all()
    answers = db.query(AttemptAnswer).filter(AttemptAnswer.attempt_id == attempt.id).all()

    correct_count = sum(1 for a in answers if a.is_correct)
    total_q = len(questions)

    comp_breakdown = {}
    for q in questions:
        cid = q.competency_id
        if cid not in comp_breakdown:
            comp_breakdown[cid] = {
                "total": 0,
                "correct": 0,
                "code": q.competency.code if q.competency else "UNKNOWN",
                "name": q.competency.name if q.competency else "Competency",
            }
        comp_breakdown[cid]["total"] += 1

    for a in answers:
        if a.is_correct:
            q = next((x for x in questions if x.id == a.question_id), None)
            if q and q.competency_id in comp_breakdown:
                comp_breakdown[q.competency_id]["correct"] += 1

    return AttemptResultResponse(
        attempt_id=attempt.id,
        assessment_id=attempt.assessment_id,
        score=attempt.score,
        total_questions=total_q,
        correct_answers=correct_count,
        competency_breakdown=comp_breakdown,
        completed_at=attempt.completed_at
    )
