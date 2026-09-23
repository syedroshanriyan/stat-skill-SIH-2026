import re
from typing import Dict, Any, Tuple


LEGAL_INTENT_CATEGORIES = [
    "informational",
    "statute_lookup",
    "section_lookup",
    "definition",
    "procedural",
    "comparative",
    "case_law_reference",
    "compliance",
    "ambiguous",
    "unsupported_high_risk"
]


def is_legal_domain_query(text: str) -> bool:
    """Detect if a user message concerns statutory, regulatory, or legal compliance matters."""
    lower = text.lower()
    legal_keywords = [
        "law", "act", "statute", "section", "article", "rule", "penalty", "punishment",
        "dpdp", "data protection", "fiduciary", "consent", "offence", "jurisdiction",
        "ministry", "subordinate legislation", "compliance", "gazette", "court",
        "statistics act", "legal", "liability", "breach", "enactment", "commencement"
    ]
    return any(re.search(r"\b" + re.escape(k) + r"\b", lower) for k in legal_keywords)


def classify_legal_query(text: str) -> Dict[str, Any]:
    """
    Classify query into one of the 10 canonical legal categories per Requirement 16:
    - informational
    - statute_lookup
    - section_lookup
    - definition
    - procedural
    - comparative
    - case_law_reference
    - compliance
    - ambiguous
    - unsupported_high_risk
    """
    lower = text.lower()

    # 1. High-risk or unsupported legal advice queries
    high_risk_patterns = [
        "represent me in court", "file a lawsuit for me", "draft my will", "legal loophole",
        "evade taxes", "bypass data protection", "help me commit", "guarantee victory in court"
    ]
    if any(p in lower for p in high_risk_patterns):
        return {
            "category": "unsupported_high_risk",
            "confidence": 0.95,
            "requires_disclaimer": True,
            "is_supported": False,
            "explanation": "Query seeks prohibited legal advice or actions outside legal-information scope."
        }

    # 2. Ambiguous query (lacks Act name, section, jurisdiction, or context)
    ambiguous_patterns = [
        r"^what is the punishment\??$",
        r"^what is the penalty\??$",
        r"^is it illegal\??$",
        r"^can i do this\??$",
        r"^what are the rules\??$",
        r"^what does the law say\??$",
        r"^how much fine\??$",
        r"^who is liable\??$"
    ]
    if any(re.match(p, lower.strip()) for p in ambiguous_patterns) or (len(lower.split()) <= 4 and ("punishment" in lower or "fine" in lower or "penalty" in lower) and not any(k in lower for k in ["dpdp", "statistics", "act", "section", "2023", "2008"])):
        return {
            "category": "ambiguous",
            "confidence": 0.90,
            "requires_clarification": True,
            "is_supported": True,
            "explanation": "Query lacks specific statute, section, jurisdiction, or factual context."
        }

    # 3. Comparative
    if any(w in lower for w in ["difference between", "compare", "versus", "vs", "amended from"]):
        return {
            "category": "comparative",
            "confidence": 0.86,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Comparative statutory or version analysis query."
        }

    # 4. Definition
    if any(w in lower for w in ["define", "what is meant by", "meaning of", "definition of"]):
        return {
            "category": "definition",
            "confidence": 0.88,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Statutory term definition query."
        }

    # 5. Procedural
    if any(w in lower for w in ["how to file", "procedure for", "process to", "steps for", "appeal process", "timeline to"]):
        return {
            "category": "procedural",
            "confidence": 0.85,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Administrative or legal procedural workflow query."
        }

    # 6. Compliance
    if any(w in lower for w in ["compliance", "audit", "dpdp rules", "safeguard", "obligation", "duty of"]):
        return {
            "category": "compliance",
            "confidence": 0.89,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Regulatory compliance and obligations query."
        }

    # 7. Section Lookup
    if re.search(r"\bsection\s+\d+\b", lower) or re.search(r"\barticle\s+\d+\b", lower) or re.search(r"\brule\s+\d+\b", lower):
        return {
            "category": "section_lookup",
            "confidence": 0.95,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Direct lookup for specific section, article, or rule."
        }

    # 8. Statute Lookup
    if any(k in lower for k in ["dpdp act", "collection of statistics act", "data protection act", "act no"]):
        if any(w in lower for w in ["what is", "overview", "summary", "enactment", "when was", "scope of"]):
            return {
                "category": "statute_lookup",
                "confidence": 0.92,
                "requires_clarification": False,
                "is_supported": True,
                "explanation": "General statute or legislative overview lookup."
            }

    # 9. Case Law / Precedent Reference
    if any(w in lower for w in ["case law", "judgment", "supreme court", "high court", "precedent", "ruling"]):
        return {
            "category": "case_law_reference",
            "confidence": 0.82,
            "requires_clarification": False,
            "is_supported": True,
            "explanation": "Inquiry regarding judicial interpretation or precedents."
        }

    # 10. Default Informational
    return {
        "category": "informational",
        "confidence": 0.75,
        "requires_clarification": False,
        "is_supported": True,
        "explanation": "General legal/statutory informational query."
    }
