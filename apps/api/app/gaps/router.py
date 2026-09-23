from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.gap import SkillGap
from app.models.competency import Competency
from app.schemas.gap import SkillGapResponse
from app.gaps.service import recalculate_user_skill_gaps

router = APIRouter(prefix="/me/gaps", tags=["Gaps"])


@router.get("", response_model=List[SkillGapResponse])
def get_my_gaps(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Recalculate to ensure state is fresh
    recalculate_user_skill_gaps(db, current_user.id)

    gaps = (
        db.query(SkillGap)
        .filter(SkillGap.user_id == current_user.id)
        .join(Competency)
        .order_by(
            # Sort critical first, then high, medium, low
            SkillGap.gap_value.desc()
        )
        .all()
    )
    return gaps


@router.get("/{gap_id}", response_model=SkillGapResponse)
def get_gap_detail(
    gap_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    gap = db.query(SkillGap).filter(
        SkillGap.id == gap_id,
        SkillGap.user_id == current_user.id
    ).first()
    if not gap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill gap not found")
    return gap
