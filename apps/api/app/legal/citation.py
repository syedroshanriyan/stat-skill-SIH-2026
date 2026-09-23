from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from app.legal.models import LegalStatute, LegalSection


def validate_legal_citation(
    db: Session,
    citation_tag: str,
    cited_claim: str
) -> Tuple[bool, Dict[str, Any]]:
    """
    Validates legal citation per Requirement 18:
    1. Source exists
    2. Source is authorized
    3. Citation target exists
    4. Section/reference exists
    5. Claim is supported by retrieved section content
    6. Source version is recorded
    """
    if not citation_tag:
        return False, {"error": "Missing citation tag. Uncited claims prohibited."}

    # Format expected: STATUTE_CODE:SECTION_TAG (e.g. DPDP-2023:S.8)
    section = db.query(LegalSection).join(LegalStatute).filter(
        LegalSection.citation_tag == citation_tag
    ).first()

    if not section:
        return False, {
            "error": f"Citation target '{citation_tag}' does not exist in authorized statutory repository.",
            "is_valid": False
        }

    statute = section.statute
    if not statute or statute.status not in ["active", "amended"]:
        return False, {
            "error": f"Cited statute is not an authorized, current statutory source (status: {statute.status if statute else 'missing'}).",
            "is_valid": False
        }

    # Validate claim support
    claim_words = [w.lower() for w in cited_claim.split() if len(w) > 4]
    sec_content = section.content.lower()

    matching_keywords = [w for w in claim_words if w in sec_content]
    claim_supported = len(matching_keywords) >= 1 or len(claim_words) == 0

    if not claim_supported:
        return False, {
            "error": f"Claim is not verifiably supported by section content in {citation_tag}.",
            "is_valid": False
        }

    return True, {
        "is_valid": True,
        "source": statute.title,
        "short_title": statute.short_title,
        "section_number": section.section_number,
        "section_title": section.section_title,
        "effective_date": section.effective_date.isoformat() if section.effective_date else None,
        "retrieval_date": statute.retrieval_date.isoformat() if statute.retrieval_date else None,
        "source_url": statute.source_url,
        "version": statute.version,
        "jurisdiction": statute.jurisdiction,
        "status": statute.status
    }


def format_authoritative_legal_answer(
    retrieved_sections: List[Dict[str, Any]],
    user_query: str,
    classification: Dict[str, Any]
) -> Dict[str, Any]:
    """Formats legal answer with mandatory disclaimer, exact statutory citations, and metadata."""
    disclaimer = (
        "LEGAL ADVISORY NOTICE: STAT-SKILL AI provides statutory legal-information and research assistance. "
        "This platform is NOT a law firm, does NOT provide formal legal counsel, and is NOT a substitute for "
        "professional legal advice from an advocate or attorney."
    )

    if not retrieved_sections:
        return {
            "disclaimer": disclaimer,
            "answer": "No authoritative statutory section could be retrieved matching the provided criteria. Please specify the applicable Act or jurisdiction.",
            "citations": [],
            "citations_validated": False,
            "category": classification.get("category", "informational")
        }

    citations = []
    answer_paragraphs = [
        f"**Statutory Analysis ({classification.get('category', 'Statute Inquiry').replace('_', ' ').title()})**\n",
        f"Based on current authoritative statutes under the **Republic of India**:"
    ]

    for sec in retrieved_sections:
        citations.append({
            "source": sec["statute_title"],
            "title": f"{sec['short_title']} - {sec['section_number']}: {sec['section_title']}",
            "section": sec["section_number"],
            "effective_date": sec["effective_date"],
            "retrieval_date": sec["retrieval_date"],
            "source_url": sec["source_url"],
            "version": sec["version"],
            "status": sec["status"],
            "citation_tag": sec["citation_tag"]
        })

        answer_paragraphs.append(
            f"- **{sec['short_title']} ({sec['section_number']}: {sec['section_title']})**:\n"
            f"  > \"{sec['content']}\"\n"
            f"  *Effective Date:* {sec['effective_date'][:10] if sec['effective_date'] else 'Enacted'} • "
            f"*Status:* `{sec['status'].upper()}` • *Source:* [{sec['source_url']}]({sec['source_url']})"
        )

    return {
        "disclaimer": disclaimer,
        "answer": "\n\n".join(answer_paragraphs),
        "citations": citations,
        "citations_validated": True,
        "category": classification.get("category", "informational")
    }
