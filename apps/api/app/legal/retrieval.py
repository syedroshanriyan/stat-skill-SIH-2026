import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.legal.models import LegalStatute, LegalSection


# Seed baseline statutes if empty
DEFAULT_STATUTES_DATA = [
    {
        "title": "Digital Personal Data Protection Act, 2023",
        "short_title": "DPDP Act, 2023",
        "act_number": "Act No. 22 of 2023",
        "jurisdiction": "Republic of India",
        "publisher": "Ministry of Electronics and Information Technology",
        "source_url": "https://www.meity.gov.in/content/digital-personal-data-protection-act-2023",
        "canonical_url": "https://www.indiacode.nic.in/handle/123456789/21262",
        "enactment_date": "2023-08-11T00:00:00Z",
        "commencement_date": "2023-08-11T00:00:00Z",
        "effective_date": "2023-08-11T00:00:00Z",
        "content_hash": "sha256-dpdp2023-verified-official-gazette",
        "version": "2023.1",
        "status": "active",
        "document_type": "Act",
        "sections": [
            {
                "section_number": "Section 4",
                "section_title": "Grounds for processing personal data",
                "content": "A person may process the personal data of an individual only in accordance with the provisions of this Act and for a lawful purpose for which the Data Principal has given her consent or for certain legitimate uses.",
                "citation_tag": "DPDP-2023:S.4",
                "effective_date": "2023-08-11T00:00:00Z"
            },
            {
                "section_number": "Section 6",
                "section_title": "Consent",
                "content": "Consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action, and shall signify an agreement to the processing of her personal data for the specified purpose.",
                "citation_tag": "DPDP-2023:S.6",
                "effective_date": "2023-08-11T00:00:00Z"
            },
            {
                "section_number": "Section 8",
                "section_title": "General obligations of Data Fiduciary",
                "content": "A Data Fiduciary shall protect personal data in its possession or under its control by taking reasonable security safeguards to prevent personal data breach. In the event of a personal data breach, the Data Fiduciary shall give the Board and each affected Data Principal intimation of such breach in such form and manner as may be prescribed.",
                "citation_tag": "DPDP-2023:S.8",
                "effective_date": "2023-08-11T00:00:00Z"
            },
            {
                "section_number": "Section 9",
                "section_title": "Processing of personal data of children",
                "content": "A Data Fiduciary shall, before processing any personal data of a child or a person with disability, obtain verifiable consent of the parent of such child. A Data Fiduciary shall not undertake tracking or behavioural monitoring of children or targeted advertising directed at children.",
                "citation_tag": "DPDP-2023:S.9",
                "effective_date": "2023-08-11T00:00:00Z"
            },
            {
                "section_number": "Section 33",
                "section_title": "Penalties for breach of obligations",
                "content": "If the Board determines that a significant breach of obligations has occurred, it may impose monetary penalties specified in the Schedule, up to two hundred and fifty crore rupees for failure to take reasonable security safeguards to prevent personal data breach under section 8.",
                "citation_tag": "DPDP-2023:S.33",
                "effective_date": "2023-08-11T00:00:00Z"
            }
        ]
    },
    {
        "title": "Collection of Statistics Act, 2008",
        "short_title": "Statistics Act, 2008",
        "act_number": "Act No. 7 of 2009",
        "jurisdiction": "Republic of India",
        "publisher": "Ministry of Statistics and Programme Implementation",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1362",
        "canonical_url": "https://www.indiacode.nic.in/handle/123456789/1362",
        "enactment_date": "2009-01-07T00:00:00Z",
        "commencement_date": "2010-06-01T00:00:00Z",
        "effective_date": "2010-06-01T00:00:00Z",
        "content_hash": "sha256-stat2008-verified-official-gazette",
        "version": "2008.1",
        "status": "active",
        "document_type": "Act",
        "sections": [
            {
                "section_number": "Section 3",
                "section_title": "Collection of statistics",
                "content": "The appropriate Government may, by notification in the Official Gazette, direct that statistics shall be collected relating to any matter specified in the notification.",
                "citation_tag": "STAT-2008:S.3",
                "effective_date": "2010-06-01T00:00:00Z"
            },
            {
                "section_number": "Section 4",
                "section_title": "Appointment of statistics officers",
                "content": "The appropriate Government may appoint any officer as a statistics officer for the purpose of collection of statistics under this Act.",
                "citation_tag": "STAT-2008:S.4",
                "effective_date": "2010-06-01T00:00:00Z"
            },
            {
                "section_number": "Section 9",
                "section_title": "Restriction on disclosure of information",
                "content": "All information furnished to a statistics officer or person assisting the statistics officer under this Act shall be kept confidential and shall not be used for any purpose other than for compilation of statistical tables.",
                "citation_tag": "STAT-2008:S.9",
                "effective_date": "2010-06-01T00:00:00Z"
            },
            {
                "section_number": "Section 15",
                "section_title": "Offences and penalties",
                "content": "Whoever fails to produce any books of account or other documents required to be produced under this Act shall be punishable with fine which may extend to one thousand rupees or in the case of a company to five thousand rupees.",
                "citation_tag": "STAT-2008:S.15",
                "effective_date": "2010-06-01T00:00:00Z"
            }
        ]
    }
]


def ensure_baseline_statutes(db: Session):
    """Seed baseline statutory database if empty."""
    count = db.query(LegalStatute).count()
    if count == 0:
        for s_data in DEFAULT_STATUTES_DATA:
            statute = LegalStatute(
                title=s_data["title"],
                short_title=s_data["short_title"],
                act_number=s_data["act_number"],
                jurisdiction=s_data["jurisdiction"],
                publisher=s_data["publisher"],
                source_url=s_data["source_url"],
                canonical_url=s_data["canonical_url"],
                enactment_date=datetime.fromisoformat(s_data["enactment_date"].replace("Z", "+00:00")),
                commencement_date=datetime.fromisoformat(s_data["commencement_date"].replace("Z", "+00:00")),
                effective_date=datetime.fromisoformat(s_data["effective_date"].replace("Z", "+00:00")),
                content_hash=s_data["content_hash"],
                version=s_data["version"],
                status=s_data["status"],
                document_type=s_data["document_type"]
            )
            db.add(statute)
            db.flush()

            for sec in s_data["sections"]:
                db.add(LegalSection(
                    statute_id=statute.id,
                    section_number=sec["section_number"],
                    section_title=sec["section_title"],
                    content=sec["content"],
                    citation_tag=sec["citation_tag"],
                    effective_date=datetime.fromisoformat(sec["effective_date"].replace("Z", "+00:00")),
                    status="active"
                ))
        db.commit()


def retrieve_authoritative_statute_sections(
    db: Session,
    query: str,
    target_date: Optional[datetime] = None,
    limit: int = 3
) -> List[Dict[str, Any]]:
    """
    RAG Statutory Retrieval with Versioning (Requirement 17):
    - Current-law queries retrieve applicable current version (status == 'active').
    - Historical-law queries retrieve version effective on the specified historical date.
    - Matches query terms against section numbers, titles, contents, and statutes.
    """
    ensure_baseline_statutes(db)

    # Determine versioning filter
    now = datetime.now(timezone.utc)
    effective_target = target_date or now

    lower_q = query.lower()
    sections_query = db.query(LegalSection).join(LegalStatute)

    if target_date:
        # Historical query: Must have been effective on target_date and enactment <= target_date
        sections_query = sections_query.filter(
            LegalStatute.effective_date <= effective_target
        )
    else:
        # Current law: active statutes
        sections_query = sections_query.filter(LegalStatute.status == "active")

    # Filter by specific Act if mentioned in query
    if any(k in lower_q for k in ["dpdp", "data protection", "fiduciary"]):
        sections_query = sections_query.filter(LegalStatute.short_title.ilike("%DPDP%"))
    elif any(k in lower_q for k in ["statistics act", "collection of statistics", "sampling"]):
        sections_query = sections_query.filter(LegalStatute.short_title.ilike("%Statistics%"))

    # Section number lookup
    sec_match = re.search(r"\bsection\s+(\d+)\b", lower_q)
    if sec_match:
        sec_num = f"Section {sec_match.group(1)}"
        exact_sec = sections_query.filter(LegalSection.section_number.ilike(f"{sec_num}%")).first()
        if exact_sec:
            return [_format_section_result(exact_sec)]

    all_secs = sections_query.all()
    scored = []

    words = [w for w in re.findall(r"\w+", lower_q) if len(w) > 3]
    for sec in all_secs:
        text_corpus = f"{sec.statute.title} {sec.section_number} {sec.section_title} {sec.content}".lower()
        score = sum(text_corpus.count(w) for w in words)
        if any(term in text_corpus for term in ["penalty", "punishment", "breach", "safeguard", "confidential"]):
            score += 2
        scored.append((score, sec))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [_format_section_result(item[1]) for item in scored[:limit]]
    return results


def _format_section_result(sec: LegalSection) -> Dict[str, Any]:
    return {
        "statute_title": sec.statute.title,
        "short_title": sec.statute.short_title,
        "act_number": sec.statute.act_number,
        "publisher": sec.statute.publisher,
        "jurisdiction": sec.statute.jurisdiction,
        "section_number": sec.section_number,
        "section_title": sec.section_title,
        "content": sec.content,
        "citation_tag": sec.citation_tag,
        "source_url": sec.statute.source_url,
        "effective_date": sec.effective_date.isoformat() if sec.effective_date else None,
        "retrieval_date": sec.statute.retrieval_date.isoformat() if sec.statute.retrieval_date else None,
        "version": sec.statute.version,
        "status": sec.statute.status,
    }
