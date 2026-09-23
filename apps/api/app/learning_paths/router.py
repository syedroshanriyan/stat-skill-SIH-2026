from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.learning_path import LearningPath, LearningPathItem
from app.models.recommendation import LearningResource, ResourceCompetency, Recommendation
from app.models.audit import AuditEvent
from app.schemas.learning_path import (
    LearningPathResponse,
    CreateLearningPathRequest,
    UpdateLearningPathItemRequest,
    LearningPathItemResponse,
)

router = APIRouter(tags=["LearningPaths"])


@router.get("/me/learning-paths", response_model=List[LearningPathResponse])
def get_my_learning_paths(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    paths = db.query(LearningPath).filter(LearningPath.user_id == current_user.id).all()

    # If no paths exist, auto-generate one from top recommendations
    if not paths:
        recs = (
            db.query(Recommendation)
            .filter(Recommendation.user_id == current_user.id)
            .order_by(Recommendation.score.desc())
            .limit(5)
            .all()
        )
        if recs:
            new_path = LearningPath(
                user_id=current_user.id,
                title="Target Competency Capacity Building Roadmap",
                goal="Systematic mastery of official & technical core competencies",
                status="active"
            )
            db.add(new_path)
            db.flush()

            for seq, rec in enumerate(recs, start=1):
                item = LearningPathItem(
                    learning_path_id=new_path.id,
                    resource_id=rec.resource_id,
                    competency_id=rec.competency_id,
                    sequence=seq,
                    status="in_progress" if seq == 1 else "pending"
                )
                db.add(item)
            db.commit()
            paths = [new_path]

    return paths


@router.post("/me/learning-paths", response_model=LearningPathResponse, status_code=status.HTTP_201_CREATED)
def create_learning_path(
    payload: CreateLearningPathRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_path = LearningPath(
        user_id=current_user.id,
        title=payload.title,
        goal=payload.goal,
        status="active"
    )
    db.add(new_path)
    db.flush()

    for idx, res_id in enumerate(payload.resource_ids, start=1):
        res = db.query(LearningResource).filter(LearningResource.id == res_id).first()
        if not res:
            continue
        rc = db.query(ResourceCompetency).filter(ResourceCompetency.resource_id == res.id).first()
        comp_id = rc.competency_id if rc else None

        item = LearningPathItem(
            learning_path_id=new_path.id,
            resource_id=res.id,
            competency_id=comp_id,
            sequence=idx,
            status="pending"
        )
        db.add(item)

    db.add(AuditEvent(
        actor_id=current_user.id,
        action="LEARNING_PATH_CREATED",
        entity_type="LEARNING_PATH",
        entity_id=new_path.id,
        metadata_json={"title": new_path.title}
    ))
    db.commit()
    db.refresh(new_path)
    return new_path


@router.get("/learning-paths/{path_id}", response_model=LearningPathResponse)
def get_learning_path(
    path_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == current_user.id
    ).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
    return path


@router.patch("/learning-paths/{path_id}/items/{item_id}", response_model=LearningPathItemResponse)
def update_learning_path_item(
    path_id: str,
    item_id: str,
    payload: UpdateLearningPathItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    path = db.query(LearningPath).filter(
        LearningPath.id == path_id,
        LearningPath.user_id == current_user.id
    ).first()
    if not path:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")

    item = db.query(LearningPathItem).filter(
        LearningPathItem.id == item_id,
        LearningPathItem.learning_path_id == path.id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path item not found")

    item.status = payload.status
    db.add(AuditEvent(
        actor_id=current_user.id,
        action="LEARNING_PATH_ITEM_UPDATED",
        entity_type="LEARNING_PATH_ITEM",
        entity_id=item.id,
        metadata_json={"status": item.status}
    ))
    db.commit()
    db.refresh(item)
    return item
