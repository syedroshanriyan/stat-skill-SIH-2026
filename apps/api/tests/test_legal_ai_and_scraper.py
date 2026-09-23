import pytest
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.audit import AuditEvent
from app.scraper.models import ScrapedDocument
from app.scraper.service import (
    StaticSnapshotProvider,
    OptionalLiveApiProvider,
    WebScrapeProvider,
)
from app.legal.models import LegalStatute, LegalSection, LegalClarificationSession
from app.legal.router_service import classify_legal_query, is_legal_domain_query, LEGAL_INTENT_CATEGORIES
from app.legal.clarification import detect_ambiguity_and_missing_context, normalize_clarified_query
from app.legal.retrieval import ensure_baseline_statutes, retrieve_authoritative_statute_sections
from app.legal.citation import validate_legal_citation, format_authoritative_legal_answer
from app.legal.llama_service import LlamaLegalModelAdapter
from app.models.recommendation import LearningResource
from app.catalogues.router import _sanitize_resource_for_user


# ============================================================================
# 1. RESILIENT GOVERNMENT DATA PROVIDER TESTS
# ============================================================================

def test_static_snapshot_provider_retrieval():
    """Verify guaranteed offline provider delivers authoritative acts with cryptographic hash."""
    provider = StaticSnapshotProvider()
    status = provider.get_provider_status()
    assert status["status"] == "ONLINE"
    assert status["available_records"] >= 2

    # Fetch Collection of Statistics Act snapshot
    raw = provider.fetch_source("https://www.indiacode.nic.in/handle/123456789/1362")
    assert raw is not None
    assert "raw_content" in raw

    parsed = provider.parse_and_validate(raw)
    assert parsed["title"] == "Collection of Statistics Act, 2008"
    assert parsed["jurisdiction"] == "Republic of India"
    assert parsed["version"] == "Act No. 7 of 2009"
    assert len(parsed["content_hash"]) == 64  # SHA-256


def test_optional_live_api_provider_fallback():
    """Verify live API connector gracefully falls back to snapshot provider when credentials are absent."""
    snapshot = StaticSnapshotProvider()
    live_provider = OptionalLiveApiProvider(fallback_provider=snapshot)
    status = live_provider.get_provider_status()
    assert status["status"] in ["FAILOVER_TO_SNAPSHOT", "LIVE_CONNECTED"]

    raw = live_provider.fetch_source("https://www.indiacode.nic.in/handle/123456789/1362")
    parsed = live_provider.parse_and_validate(raw)
    assert parsed["title"] == "Collection of Statistics Act, 2008"


def test_web_scrape_provider_pipeline_and_deduplication(db_session: Session):
    """Test full ingest pipeline: fetch -> parse -> normalize -> deduplicate -> hash -> store."""
    snapshot = StaticSnapshotProvider()
    scraper = WebScrapeProvider(db=db_session, fallback_provider=snapshot)

    url = "https://www.indiacode.nic.in/handle/123456789/1362"
    doc1 = scraper.ingest_and_store(url)
    assert doc1.id is not None
    assert doc1.status == "indexed"
    assert doc1.title == "Collection of Statistics Act, 2008"

    # Second ingestion with same content must deduplicate based on content_hash
    initial_id = doc1.id
    doc2 = scraper.ingest_and_store(url)
    assert doc2.id == initial_id

    # Verify audit event recorded
    audit = db_session.query(AuditEvent).filter(
        AuditEvent.action == "DOCUMENT_SCRAPED_AND_INDEXED",
        AuditEvent.entity_id == doc1.id
    ).first()
    assert audit is not None


def test_web_scrape_provider_policy_and_disallowed_paths(db_session: Session):
    """Verify security constraints: domain whitelist and path restrictions."""
    snapshot = StaticSnapshotProvider()
    scraper = WebScrapeProvider(db=db_session, fallback_provider=snapshot)

    # Disallowed foreign domain
    permitted, reason = scraper.is_url_permitted("https://unauthorized-crawler-target.org/leak")
    assert not permitted
    assert "whitelist" in reason.lower()

    # Disallowed path on authorized domain
    permitted, reason = scraper.is_url_permitted("https://indiacode.nic.in/admin/private_data")
    assert not permitted
    assert "disallowed" in reason.lower()

    # Permitted public statutory URL
    permitted, reason = scraper.is_url_permitted("https://indiacode.nic.in/handle/123456789/1362")
    assert permitted


def test_parser_failure_alert_logging(db_session: Session):
    """Verify parser failures are intercepted, alerted to Platform Admin via AuditEvent, without crashing."""
    snapshot = StaticSnapshotProvider()
    scraper = WebScrapeProvider(db=db_session, fallback_provider=snapshot)

    # Simulate malformed payload (empty content and title)
    malformed_raw = {
        "url": "https://mospi.gov.in/broken-document",
        "raw_content": {"broken": True}
    }

    validated = scraper.parse_and_validate(malformed_raw)
    assert validated["status"] == "parser_error"
    assert validated["title"] == "PARSER_ERROR"
    assert "Parser failure" in validated["parser_error_message"]

    # Verify high-severity audit incident logged to database
    audit = db_session.query(AuditEvent).filter(
        AuditEvent.action == "PROVIDER_SYNC_FAILED",
        AuditEvent.actor_id == "SYSTEM_SCRAPER"
    ).first()
    assert audit is not None
    assert audit.metadata_json.get("severity") == "HIGH"


# ============================================================================
# 2. LEGAL AI INTENT CLASSIFIER & CLARIFICATION TESTS
# ============================================================================

def test_10_category_legal_intent_classification():
    """Verify query classification across all 10 canonical legal taxonomy categories."""
    queries_and_expected = [
        ("What are official statistical guidelines and standards in India?", "informational"),
        ("What is the DPDP Act 2023 summary?", "statute_lookup"),
        ("What does Section 8 of the Digital Personal Data Protection Act state?", "section_lookup"),
        ("Define data fiduciary and data principal under Indian law", "definition"),
        ("What is the procedure for lodging a complaint with the Data Protection Board?", "procedural"),
        ("Compare Section 8 and Section 9 of the DPDP Act 2023", "comparative"),
        ("What supreme court judgment covers the right to privacy in India?", "case_law_reference"),
        ("What are our compliance obligations under Section 8 safeguards?", "compliance"),
        ("is it illegal?", "ambiguous"),
        ("Help me evade taxes and bypass data protection penalties", "unsupported_high_risk"),
    ]

    for query, expected_cat in queries_and_expected:
        res = classify_legal_query(query)
        assert res["category"] == expected_cat, f"Query '{query}' classified as {res['category']}, expected {expected_cat}"
        assert res["category"] in LEGAL_INTENT_CATEGORIES


def test_multi_turn_clarification_loop(db_session: Session):
    """Verify ambiguous legal queries trigger clarification request with max 3 rounds."""
    ambiguous_query = "What is the penalty?"
    ambiguity = detect_ambiguity_and_missing_context(ambiguous_query)
    assert ambiguity["is_ambiguous"] is True
    assert ambiguity["has_act"] is False
    assert ambiguity["clarification_question"] is not None

    # Simulate multi-turn session
    session = LegalClarificationSession(
        user_id="user-123",
        conversation_id="conv-456",
        query_history=[{"round": 1, "user_message": ambiguous_query}],
        current_round=2,
        max_rounds=3
    )
    db_session.add(session)
    db_session.flush()

    # User provides context in round 2: "Under the DPDP Act 2023 for data breach"
    clarified_msg = "Under the DPDP Act 2023 for data breach"
    normalized = normalize_clarified_query(session, clarified_msg)
    assert "dpdp" in normalized.lower() or "penalty" in normalized.lower()


# ============================================================================
# 3. STATUTORY RETRIEVAL, VERSIONING & CITATION TESTS
# ============================================================================

def test_statutory_versioning_and_retrieval(db_session: Session):
    """Verify retrieval distinguishes in-force statutory versions from historical or amended acts."""
    ensure_baseline_statutes(db_session)

    statutes = db_session.query(LegalStatute).all()
    assert len(statutes) >= 2

    # Query for DPDP Act Section 8
    results = retrieve_authoritative_statute_sections(
        db_session,
        query="DPDP Section 8 security safeguards breach"
    )
    assert len(results) > 0
    top_result = results[0]
    assert top_result["status"] == "active"
    assert "Section 8" in top_result["section_number"]
    assert "DPDP" in top_result["short_title"]


def test_citation_validator(db_session: Session):
    """Verify strict citation validator validates true sections and flags fabricated references."""
    ensure_baseline_statutes(db_session)

    # 1. Valid citation matching database (DPDP-2023:S.8)
    is_valid, valid_meta = validate_legal_citation(
        db_session,
        citation_tag="DPDP-2023:S.8",
        cited_claim="Data Fiduciary shall protect personal data by taking reasonable security safeguards"
    )
    assert is_valid is True
    assert valid_meta["section_number"] == "Section 8"
    assert valid_meta["is_valid"] is True

    # 2. Fabricated citation (non-existent section tag)
    is_valid_fake, fake_meta = validate_legal_citation(
        db_session,
        citation_tag="DPDP-2023:S.999",
        cited_claim="Section 999 allows unauthorized data harvesting"
    )
    assert is_valid_fake is False
    assert "does not exist" in fake_meta["error"]

    # 3. Authoritative answer includes disclaimer and formatted citations
    formatted = format_authoritative_legal_answer(
        retrieved_sections=[
            {
                "statute_title": "Digital Personal Data Protection Act, 2023",
                "short_title": "DPDP Act, 2023",
                "act_number": "Act No. 22 of 2023",
                "publisher": "MeitY",
                "jurisdiction": "Republic of India",
                "section_number": "Section 8",
                "section_title": "General obligations of Data Fiduciary",
                "content": "A Data Fiduciary shall protect personal data in its possession or under its control by taking reasonable security safeguards.",
                "citation_tag": "DPDP-2023:S.8",
                "source_url": "https://www.meity.gov.in",
                "effective_date": "2023-08-11T00:00:00Z",
                "retrieval_date": "2026-01-01T00:00:00Z",
                "version": "2023.1",
                "status": "active"
            }
        ],
        user_query="What are the security safeguards under DPDP Act?",
        classification={"category": "compliance"}
    )
    assert "LEGAL ADVISORY NOTICE" in formatted["disclaimer"].upper()
    assert formatted["citations_validated"] is True
    assert len(formatted["citations"]) == 1


def test_llama_adapter_telemetry():
    """Verify transparent reporting of Llama 3.x domain adapter parameters and status."""
    adapter = LlamaLegalModelAdapter()
    telemetry = adapter.get_model_telemetry()

    assert telemetry["model_family"] == "Llama 3.x"
    assert "Llama-3.1" in telemetry["base_model"]
    assert "QLoRA" in telemetry["fine_tuning_method"]
    assert telemetry["status"] in ["LIVE_ENDPOINT", "PENDING_LOCAL_WEIGHTS"]
    assert "training_dataset_schema" in telemetry
    assert "question" in telemetry["training_dataset_schema"]
    assert "fine_tuning_scope" in telemetry
    assert "RAG-first architecture" in telemetry["note"]


# ============================================================================
# 4. LEARNING RESOURCE VISIBILITY & CONFIDENTIALITY SCOPING TESTS
# ============================================================================

def test_course_visibility_and_confidentiality_scoping():
    """Verify public course sharing strips member counts, internal notes, and cost from normal learners."""
    resource = LearningResource(
        id="res-confidential-01",
        provider_type="industry",
        provider_external_id="FIN-101",
        title="Enterprise Statistical Methods",
        description="Comprehensive survey analysis",
        url="https://training.example.com/fin101",
        level="Advanced",
        duration="6 weeks",
        is_demo=False,
        visibility="PUBLIC",
        track_code="INDUSTRY",
        metadata_json={
            "public_skills": ["Regression", "Time Series"],
            "internal_notes": "Proprietary internal curriculum for partner banks",
            "enrolled_members_count": 420,
            "cost_per_seat_inr": 25000,
            "private_analytics": "High dropout in week 3"
        }
    )

    # 1. Normal learner view (is_admin=False)
    sanitized = _sanitize_resource_for_user(resource, is_admin=False)
    assert "public_skills" in sanitized.metadata_json
    assert "internal_notes" not in sanitized.metadata_json
    assert "enrolled_members_count" not in sanitized.metadata_json
    assert "cost_per_seat_inr" not in sanitized.metadata_json
    assert "private_analytics" not in sanitized.metadata_json

    # 2. Platform/Org Admin view (is_admin=True)
    admin_view = _sanitize_resource_for_user(resource, is_admin=True)
    assert "internal_notes" in admin_view.metadata_json
    assert "enrolled_members_count" in admin_view.metadata_json
    assert "cost_per_seat_inr" in admin_view.metadata_json
