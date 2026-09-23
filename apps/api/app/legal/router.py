import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user, get_auth_context, AuthContext
from app.models.user import User
from app.legal.models import LegalStatute, LegalSection, LegalClarificationSession
from app.legal.router_service import classify_legal_query, is_legal_domain_query
from app.legal.clarification import detect_ambiguity_and_missing_context, normalize_clarified_query
from app.legal.retrieval import retrieve_authoritative_statute_sections, ensure_baseline_statutes
from app.legal.citation import validate_legal_citation, format_authoritative_legal_answer
from app.legal.llama_service import llama_adapter
from app.scraper.service import WebScrapeProvider, StaticSnapshotProvider

router = APIRouter(prefix="/legal", tags=["Legal AI Intelligence"])


class LegalQueryRequest(BaseModel):
    query: str
    conversation_id: Optional[str] = None
    target_effective_date: Optional[str] = None  # For historical queries, e.g. "2015-01-01"


class LegalQueryResponse(BaseModel):
    query: str
    category: str
    requires_clarification: bool
    clarification_round: int
    clarification_question: Optional[str] = None
    answer: str
    citations: List[Dict[str, Any]]
    citations_validated: bool
    disclaimer: str
    model_used: str


@router.post("/query", response_model=LegalQueryResponse)
def execute_legal_query(
    payload: LegalQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ensure_baseline_statutes(db)
    query_text = payload.query.strip()
    conv_id = payload.conversation_id or str(uuid.uuid4())

    # 1. Intent Classification
    classification = classify_legal_query(query_text)
    category = classification["category"]

    # Check for unsupported high-risk query
    if category == "unsupported_high_risk":
        return LegalQueryResponse(
            query=query_text,
            category=category,
            requires_clarification=False,
            clarification_round=0,
            clarification_question=None,
            answer=(
                "STAT-SKILL AI provides educational and statutory research assistance only. "
                "The requested query involves high-risk actions or formal legal representation, which cannot be provided. "
                "Please consult a certified legal advocate or attorney."
            ),
            citations=[],
            citations_validated=False,
            disclaimer="LEGAL NOTICE: STAT-SKILL AI does NOT provide legal representation or counsel.",
            model_used="STAT-SKILL Intent Guardrail"
        )

    # 2. Clarification Session Management
    session = db.query(LegalClarificationSession).filter(
        LegalClarificationSession.user_id == current_user.id,
        LegalClarificationSession.conversation_id == conv_id,
        LegalClarificationSession.is_resolved == False
    ).first()

    if not session:
        session = LegalClarificationSession(
            user_id=current_user.id,
            conversation_id=conv_id,
            query_history=[],
            current_round=1
        )
        db.add(session)
        db.flush()

    # 3. Ambiguity & Missing Context Detection (Requirement 15)
    ambiguity = detect_ambiguity_and_missing_context(query_text, session)

    if (ambiguity["is_ambiguous"] or classification.get("requires_clarification")) and session.current_round <= session.max_rounds:
        # Prompt for user clarification
        clarification_q = ambiguity["clarification_question"] or "Which specific Act or section in Indian jurisdiction are you inquiring about?"

        history = list(session.query_history or [])
        history.append({
            "round": session.current_round,
            "user_message": query_text,
            "clarification_prompted": clarification_q,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        session.query_history = history
        session.current_round += 1
        db.commit()

        return LegalQueryResponse(
            query=query_text,
            category="ambiguous",
            requires_clarification=True,
            clarification_round=session.current_round - 1,
            clarification_question=clarification_q,
            answer=f"To provide an accurate statutory reference, please clarify: {clarification_q}",
            citations=[],
            citations_validated=False,
            disclaimer="LEGAL RESEARCH ASSISTANT: Exact statutory references require specific Act and jurisdiction.",
            model_used="STAT-SKILL Clarification Loop"
        )

    # If rounds exceeded max and still ambiguous
    if ambiguity["is_ambiguous"] and session.current_round > session.max_rounds:
        session.is_resolved = True
        db.commit()
        return LegalQueryResponse(
            query=query_text,
            category="ambiguous",
            requires_clarification=False,
            clarification_round=session.current_round,
            clarification_question=None,
            answer="The information provided is insufficient to identify an authoritative statutory section. Please formulate your question with the Act title or specific legal topic.",
            citations=[],
            citations_validated=False,
            disclaimer="LEGAL RESEARCH ASSISTANT: Insufficient facts for statutory retrieval.",
            model_used="STAT-SKILL Clarification Loop"
        )

    # 4. Normalized Query & Authoritative Retrieval (Requirement 13 & 17)
    normalized_query = normalize_clarified_query(session, query_text)

    target_date = None
    if payload.target_effective_date:
        try:
            target_date = datetime.fromisoformat(payload.target_effective_date.replace("Z", "+00:00"))
        except Exception:
            target_date = None

    retrieved = retrieve_authoritative_statute_sections(
        db=db,
        query=normalized_query,
        target_date=target_date,
        limit=3
    )

    # 5. Citation Validation (Requirement 18)
    for sec in retrieved:
        valid, meta = validate_legal_citation(db, sec["citation_tag"], sec["content"])
        sec["is_citation_valid"] = valid

    # Format result with disclaimer and authoritative citations
    formatted = format_authoritative_legal_answer(retrieved, normalized_query, classification)

    session.is_resolved = True
    db.commit()

    return LegalQueryResponse(
        query=query_text,
        category=category,
        requires_clarification=False,
        clarification_round=session.current_round,
        clarification_question=None,
        answer=formatted["answer"],
        citations=formatted["citations"],
        citations_validated=formatted["citations_validated"],
        disclaimer=formatted["disclaimer"],
        model_used=f"Legal RAG + Llama Domain Adapter ({llama_adapter.base_model})"
    )


@router.get("/statutes")
def list_statutes(db: Session = Depends(get_db)):
    ensure_baseline_statutes(db)
    statutes = db.query(LegalStatute).all()
    results = []
    for s in statutes:
        sec_count = len(s.sections)
        results.append({
            "id": s.id,
            "title": s.title,
            "short_title": s.short_title,
            "act_number": s.act_number,
            "jurisdiction": s.jurisdiction,
            "publisher": s.publisher,
            "source_url": s.source_url,
            "canonical_url": s.canonical_url,
            "effective_date": s.effective_date.isoformat() if s.effective_date else None,
            "version": s.version,
            "status": s.status,
            "sections_indexed": sec_count
        })
    return results


@router.get("/statutes/{statute_id}")
def get_statute_detail(statute_id: str, db: Session = Depends(get_db)):
    statute = db.query(LegalStatute).filter(LegalStatute.id == statute_id).first()
    if not statute:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Statute not found")

    return {
        "id": statute.id,
        "title": statute.title,
        "short_title": statute.short_title,
        "act_number": statute.act_number,
        "jurisdiction": statute.jurisdiction,
        "publisher": statute.publisher,
        "source_url": statute.source_url,
        "effective_date": statute.effective_date.isoformat() if statute.effective_date else None,
        "version": statute.version,
        "status": statute.status,
        "sections": [
            {
                "id": sec.id,
                "section_number": sec.section_number,
                "section_title": sec.section_title,
                "content": sec.content,
                "citation_tag": sec.citation_tag,
                "effective_date": sec.effective_date.isoformat() if sec.effective_date else None,
                "status": sec.status
            }
            for sec in statute.sections
        ]
    }


@router.get("/model/status")
def get_legal_model_status():
    """Returns telemetry and fine-tuning metadata for the Llama legal domain adapter."""
    return llama_adapter.get_model_telemetry()


@router.get("/scraper/status")
def get_scraper_status(db: Session = Depends(get_db)):
    """Returns scraper status, whitelisted domains, and rate limiting controls."""
    provider = WebScrapeProvider(db=db, fallback_provider=StaticSnapshotProvider())
    return provider.get_provider_status()
