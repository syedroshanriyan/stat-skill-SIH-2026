from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.recommendation import Recommendation, LearningResource
from app.models.competency import Competency
from app.models.audit import AuditEvent
from app.schemas.recommendation import RecommendationResponse
from app.recommendations.service import generate_hybrid_recommendations

router = APIRouter(tags=["Recommendations"])


@router.get("/me/recommendations", response_model=List[RecommendationResponse])
def get_my_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    generate_hybrid_recommendations(db, current_user.id)

    recs = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .join(LearningResource)
        .join(Competency)
        .order_by(Recommendation.score.desc())
        .all()
    )
    return recs


@router.post("/recommendations/{rec_id}/save", response_model=RecommendationResponse)
def save_recommendation(
    rec_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(
        Recommendation.id == rec_id,
        Recommendation.user_id == current_user.id
    ).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    rec.status = "saved"
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/recommendations/{rec_id}/dismiss", response_model=RecommendationResponse)
def dismiss_recommendation(
    rec_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(
        Recommendation.id == rec_id,
        Recommendation.user_id == current_user.id
    ).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    rec.status = "dismissed"
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/recommendations/{rec_id}/start", response_model=RecommendationResponse)
def start_recommendation(
    rec_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(
        Recommendation.id == rec_id,
        Recommendation.user_id == current_user.id
    ).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    rec.status = "started"
    db.commit()
    db.refresh(rec)
    return rec


@router.post("/recommendations/{rec_id}/complete", response_model=RecommendationResponse)
def complete_recommendation(
    rec_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(
        Recommendation.id == rec_id,
        Recommendation.user_id == current_user.id
    ).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    rec.status = "completed"
    db.add(AuditEvent(
        actor_id=current_user.id,
        action="RECOMMENDATION_COMPLETED",
        entity_type="RECOMMENDATION",
        entity_id=rec.id,
        metadata_json={"resource_id": rec.resource_id, "competency_id": rec.competency_id}
    ))
    db.commit()
    db.refresh(rec)
    return rec
