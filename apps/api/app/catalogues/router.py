from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.auth.deps import get_auth_context, AuthContext, security_scheme
from app.models.recommendation import LearningResource
from app.schemas.recommendation import LearningResourceResponse
from app.catalogues.providers import PROVIDERS

router = APIRouter(prefix="/catalogues", tags=["Catalogues"])


def _sanitize_resource_for_user(resource: LearningResource, is_admin: bool) -> LearningResourceResponse:
    """Strip private organization notes, enrollment counts, and member data from normal users."""
    meta = resource.metadata_json or {}
    if not is_admin:
        meta = {
            k: v for k, v in meta.items()
            if not any(priv in k.lower() for priv in ["member", "enrollment", "internal_note", "private_analytics", "cost"])
        }

    return LearningResourceResponse(
        id=resource.id,
        provider_type=resource.provider_type,
        provider_external_id=resource.provider_external_id,
        title=resource.title,
        description=resource.description,
        url=resource.url,
        level=resource.level or "Intermediate",
        duration=resource.duration or "4 weeks",
        is_demo=bool(resource.is_demo),
        visibility=resource.visibility or "PUBLIC",
        track_code=resource.track_code,
        metadata_json=meta
    )


@router.get("/status", response_model=List[Dict[str, Any]])
def get_providers_status():
    return [provider.get_provider_status() for provider in PROVIDERS.values()]


@router.get("/search", response_model=List[LearningResourceResponse])
def search_catalogues(
    query: Optional[str] = Query(None, description="Search term for course title or description"),
    provider: Optional[str] = Query(None, description="Provider filter: igot, nssta, industry, academia"),
    competency_id: Optional[str] = Query(None, description="Filter by competency ID"),
    visibility: Optional[str] = Query(None, description="PUBLIC, TRACK, ORGANIZATION, PRIVATE"),
    db: Session = Depends(get_db)
):
    q = db.query(LearningResource)

    if provider:
        q = q.filter(LearningResource.provider_type == provider.lower())

    if query:
        q = q.filter(
            or_(
                LearningResource.title.ilike(f"%{query}%"),
                LearningResource.description.ilike(f"%{query}%")
            )
        )

    if visibility:
        q = q.filter(LearningResource.visibility == visibility.upper())

    resources = q.all()
    # By default, public search returns sanitized public data
    return [_sanitize_resource_for_user(r, is_admin=False) for r in resources]


@router.get("/{provider}/{external_id}", response_model=LearningResourceResponse)
def get_catalogue_entry(
    provider: str,
    external_id: str,
    db: Session = Depends(get_db)
):
    p = PROVIDERS.get(provider.lower())
    if not p:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unknown provider: {provider}")

    resource = p.get_resource(db, external_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Catalogue entry not found")

    return _sanitize_resource_for_user(resource, is_admin=False)


@router.get("/resource/{resource_id}/admin-stats")
def get_resource_admin_stats(
    resource_id: str,
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
):
    """Admin-only view exposing aggregate enrollment and member statistics for authorized managers."""
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

    # Authorization check
    if not (auth.is_platform_admin or any(r in ["org_admin", "institution_admin"] for r in auth.roles)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Restricted to authorized administrators only")

    from app.models.learning_path import LearningPathItem
    enrolled_count = db.query(LearningPathItem).filter(LearningPathItem.resource_id == resource.id).count()
    completed_count = db.query(LearningPathItem).filter(
        LearningPathItem.resource_id == resource.id,
        LearningPathItem.status == "completed"
    ).count()

    return {
        "resource_id": resource.id,
        "title": resource.title,
        "visibility": resource.visibility,
        "total_enrolled_learners": enrolled_count,
        "completed_learners": completed_count,
        "completion_rate_pct": round((completed_count / enrolled_count * 100.0) if enrolled_count > 0 else 0.0, 1),
        "authorized_admin_scope": "PLATFORM_GLOBAL" if auth.is_platform_admin else "ORGANIZATION_AUTHORIZED"
    }

