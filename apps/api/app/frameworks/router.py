from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.competency import CompetencyFramework, Competency
from app.schemas.competency import FrameworkResponse, CompetencyResponse

router = APIRouter(prefix="/frameworks", tags=["Frameworks"])


@router.get("", response_model=List[FrameworkResponse])
def list_frameworks(
    track: Optional[str] = Query(None, description="Filter by track code (GOVERNMENT, INDUSTRY, ACADEMIA)"),
    db: Session = Depends(get_db)
):
    query = db.query(CompetencyFramework)
    if track:
        query = query.join(CompetencyFramework.track).filter(CompetencyFramework.track.has(code=track.upper()))

    frameworks = query.all()
    results = []
    for fw in frameworks:
        comp_count = db.query(Competency).filter(Competency.framework_id == fw.id).count()
        results.append(FrameworkResponse(
            id=fw.id,
            track_id=fw.track_id,
            name=fw.name,
            version=fw.version,
            status=fw.status,
            competencies_count=comp_count
        ))
    return results


@router.get("/{framework_id}", response_model=FrameworkResponse)
def get_framework(framework_id: str, db: Session = Depends(get_db)):
    fw = db.query(CompetencyFramework).filter(CompetencyFramework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Framework not found")

    comp_count = db.query(Competency).filter(Competency.framework_id == fw.id).count()
    return FrameworkResponse(
        id=fw.id,
        track_id=fw.track_id,
        name=fw.name,
        version=fw.version,
        status=fw.status,
        competencies_count=comp_count
    )


@router.get("/{framework_id}/competencies", response_model=List[CompetencyResponse])
def get_framework_competencies(
    framework_id: str,
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    query = db.query(Competency).filter(Competency.framework_id == framework_id)
    if category:
        query = query.filter(Competency.category == category)

    return query.order_by(Competency.code).all()
