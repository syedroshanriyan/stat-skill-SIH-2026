from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User, Role
from app.models.competency_history import CompetencyHistory
from app.schemas.competency import (
    UserCompetencyResponse,
    RoleCompetencyResponse,
    CompetencyHistoryResponse,
)

router = APIRouter(tags=["Competencies"])


@router.get("/me/competencies", response_model=List[UserCompetencyResponse])
def get_my_competencies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comps = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .join(Competency)
        .order_by(Competency.category, Competency.code)
        .all()
    )
    return comps


@router.get("/me/competencies/history", response_model=List[CompetencyHistoryResponse])
def get_competency_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Returns immutable competency change ledger ordered chronologically
    history = (
        db.query(CompetencyHistory)
        .filter(CompetencyHistory.user_id == current_user.id)
        .order_by(CompetencyHistory.timestamp.desc())
        .all()
    )
    return history


@router.get("/roles/{role_id}/competencies", response_model=List[RoleCompetencyResponse])
def get_role_competencies(
    role_id: str,
    db: Session = Depends(get_db)
):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    role_comps = (
        db.query(RoleCompetency)
        .filter(RoleCompetency.role_id == role_id)
        .join(Competency)
        .order_by(RoleCompetency.priority, Competency.code)
        .all()
    )
    return role_comps
