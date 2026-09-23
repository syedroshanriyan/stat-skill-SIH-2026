import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User
from app.models.evidence import Evidence
from app.models.competency import Competency
from app.models.audit import AuditEvent
from app.schemas.evidence import (
    CreateEvidenceRequest,
    UpdateEvidenceRequest,
    EvidenceResponse,
)

router = APIRouter(prefix="/evidence", tags=["Evidence"])


def analyze_evidence_with_ai(title: str, description: str, ev_type: str) -> dict:
    # Deterministic baseline analysis
    analysis = {
        "classification": "partially demonstrated",
        "summary": f"Evidence submitted for {title} demonstrates foundational practical application.",
        "detected_competencies": []
    }

    lower_text = f"{title} {description}".lower()

    if "python" in lower_text or "pandas" in lower_text:
        analysis["detected_competencies"].append({"code": "TECH-01", "confidence": 0.82, "rationale": "Direct mention of Python data processing and analytics libraries."})
    if "sampling" in lower_text or "survey" in lower_text:
        analysis["detected_competencies"].append({"code": "STAT-02", "confidence": 0.85, "rationale": "Practical implementation of survey or sampling methodologies."})
    if "sql" in lower_text or "query" in lower_text or "database" in lower_text:
        analysis["detected_competencies"].append({"code": "TECH-03", "confidence": 0.88, "rationale": "Demonstration of relational query writing and database manipulation."})
    if "power bi" in lower_text or "dashboard" in lower_text or "visualization" in lower_text:
        analysis["detected_competencies"].append({"code": "TECH-05", "confidence": 0.80, "rationale": "Executive reporting and visual analytics design."})

    if analysis["detected_competencies"]:
        analysis["classification"] = "demonstrated"
    else:
        analysis["classification"] = "insufficient evidence"
        analysis["summary"] = "Additional methodological details or repository links required to verify specific competency alignment."

    return analysis


@router.post("", response_model=EvidenceResponse, status_code=status.HTTP_201_CREATED)
def submit_evidence(
    payload: CreateEvidenceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ai_eval = analyze_evidence_with_ai(payload.title, payload.description, payload.type)

    evidence = Evidence(
        user_id=current_user.id,
        type=payload.type,
        title=payload.title,
        description=payload.description,
        url=payload.url,
        storage_key=payload.storage_key,
        status="ai_analyzed",
        ai_analysis_json=ai_eval
    )
    db.add(evidence)
    db.add(AuditEvent(
        actor_id=current_user.id,
        action="EVIDENCE_SUBMITTED",
        entity_type="EVIDENCE",
        entity_id=evidence.id,
        metadata_json={"title": evidence.title, "type": evidence.type}
    ))
    db.commit()
    db.refresh(evidence)
    return evidence


@router.get("", response_model=List[EvidenceResponse])
def list_my_evidence(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = db.query(Evidence).filter(Evidence.user_id == current_user.id).order_by(Evidence.created_at.desc()).all()
    return items


@router.patch("/{evidence_id}", response_model=EvidenceResponse)
def update_evidence(
    evidence_id: str,
    payload: UpdateEvidenceRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Evidence).filter(
        Evidence.id == evidence_id,
        Evidence.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence record not found")

    if payload.title is not None:
        item.title = payload.title
    if payload.description is not None:
        item.description = payload.description
    if payload.url is not None:
        item.url = payload.url
    if payload.status is not None:
        item.status = payload.status

    db.add(AuditEvent(
        actor_id=current_user.id,
        action="EVIDENCE_UPDATED",
        entity_type="EVIDENCE",
        entity_id=item.id,
        metadata_json={"status": item.status}
    ))
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{evidence_id}")
def delete_evidence(
    evidence_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Evidence).filter(
        Evidence.id == evidence_id,
        Evidence.user_id == current_user.id
    ).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evidence record not found")

    db.delete(item)
    db.commit()
    return {"message": "Evidence deleted successfully"}
