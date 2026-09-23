import re
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.legal.models import LegalClarificationSession


def detect_ambiguity_and_missing_context(text: str, session: Optional[LegalClarificationSession] = None) -> Dict[str, Any]:
    """
    Evaluates whether the query provides sufficient context:
    - Act / Statute reference
    - Jurisdiction (Union / State / India)
    - Specific offence, section, or subject matter
    """
    lower = text.lower()

    has_jurisdiction = any(j in lower for j in ["india", "central", "union", "state", "delhi", "karnataka", "maharashtra", "indian"])
    has_act = any(a in lower for a in ["dpdp", "data protection", "statistics act", "collection of statistics", "it act", "information technology"])
    has_subject = any(s in lower for s in ["penalty", "breach", "fiduciary", "consent", "confidentiality", "disclosure", "children", "microdata", "officer", "notice"])

    # If user provided historical clarification in session
    if session and session.query_history:
        for turn in session.query_history:
            prev_lower = turn.get("user_message", "").lower()
            if any(a in prev_lower for a in ["dpdp", "data protection", "statistics act", "collection of statistics"]):
                has_act = True
            if any(j in prev_lower for j in ["india", "union", "central"]):
                has_jurisdiction = True

    is_ambiguous = not (has_act or (has_subject and has_jurisdiction))

    clarification_question = None
    if is_ambiguous:
        if not has_act and not has_subject:
            clarification_question = "Which specific offence, statutory Act (such as the Digital Personal Data Protection Act, 2023 or Collection of Statistics Act, 2008), and jurisdiction are you referring to?"
        elif not has_act:
            clarification_question = "Which specific legislation or Act (e.g., DPDP Act 2023 or Collection of Statistics Act 2008) applies to your query?"
        else:
            clarification_question = "Could you specify the particular section, obligation, or factual scenario you wish to examine?"

    return {
        "is_ambiguous": is_ambiguous,
        "has_jurisdiction": has_jurisdiction,
        "has_act": has_act,
        "has_subject": has_subject,
        "clarification_question": clarification_question
    }


def normalize_clarified_query(session: LegalClarificationSession, latest_message: str) -> str:
    """Combines original ambiguous query with user's clarification turns into a normalized retrieval query."""
    history_texts = [turn.get("user_message", "") for turn in (session.query_history or [])]
    history_texts.append(latest_message)
    combined = " ".join(history_texts).strip()

    # Normalize aliases
    combined = re.sub(r"\bdpdp\b", "Digital Personal Data Protection Act 2023", combined, flags=re.IGNORECASE)
    combined = re.sub(r"\bstatistics act\b", "Collection of Statistics Act 2008", combined, flags=re.IGNORECASE)

    return combined
