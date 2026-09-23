import pytest
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, Track, Profile, Organization, Membership
from app.models.competency import CompetencyFramework, Competency, UserCompetency
from app.models.competency_history import CompetencyHistory
from app.models.gap import SkillGap
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt
from app.models.document import Document, DocumentChunk
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt
from app.quizzes.service import score_quiz_submission
from app.assessments.service import score_assessment_attempt
from app.assistant.service import answer_assistant_query


@pytest.fixture
def test_setup(db_session):
    # Setup 3 Tracks
    track_gov = Track(code="GOVERNMENT", name="Government Track")
    track_ind = Track(code="INDUSTRY", name="Industry Track")
    track_acad = Track(code="ACADEMIA", name="Academia Track")
    db_session.add_all([track_gov, track_ind, track_acad])
    db_session.flush()

    # Setup 3 Organizations
    org_gov = Organization(name="MoSPI Department", type="GOVERNMENT")
    org_ind_a = Organization(name="FinTech Corp", type="INDUSTRY")
    org_ind_b = Organization(name="HealthAnalytics Ltd", type="INDUSTRY")
    org_acad = Organization(name="National University", type="ACADEMIA")
    db_session.add_all([org_gov, org_ind_a, org_ind_b, org_acad])
    db_session.flush()

    # Setup Users: Gov Official, Industry User, Academic Student, Org Admin A, Org Admin B, Platform Admin
    pwd = get_password_hash("Password123")

    gov_user = User(email="officer@mospi.gov.in", password_hash=pwd, display_name="Gov Officer")
    ind_user = User(email="analyst@fintech.io", password_hash=pwd, display_name="Industry Analyst")
    acad_user = User(email="student@univ.edu.in", password_hash=pwd, display_name="Academic Student")
    org_admin_a = User(email="admin.a@fintech.io", password_hash=pwd, display_name="Org Admin A")
    org_admin_b = User(email="admin.b@health.io", password_hash=pwd, display_name="Org Admin B")
    plat_admin = User(email="platform.super@statskill.gov.in", password_hash=pwd, display_name="Super Admin")

    db_session.add_all([gov_user, ind_user, acad_user, org_admin_a, org_admin_b, plat_admin])
    db_session.flush()

    # Memberships
    m_gov = Membership(user_id=gov_user.id, organization_id=org_gov.id, role="official")
    m_ind = Membership(user_id=ind_user.id, organization_id=org_ind_a.id, role="professional")
    m_acad = Membership(user_id=acad_user.id, organization_id=org_acad.id, role="student")
    m_admin_a = Membership(user_id=org_admin_a.id, organization_id=org_ind_a.id, role="org_admin")
    m_admin_b = Membership(user_id=org_admin_b.id, organization_id=org_ind_b.id, role="org_admin")
    m_plat = Membership(user_id=plat_admin.id, organization_id=org_gov.id, role="platform_admin")

    db_session.add_all([m_gov, m_ind, m_acad, m_admin_a, m_admin_b, m_plat])

    # Profiles
    p_gov = Profile(user_id=gov_user.id, track_id=track_gov.id, department="Sample Design")
    p_ind = Profile(user_id=ind_user.id, track_id=track_ind.id, department="Data Engineering")
    p_acad = Profile(user_id=acad_user.id, track_id=track_acad.id, department="Computer Science")
    p_admin_a = Profile(user_id=org_admin_a.id, track_id=track_ind.id)
    p_admin_b = Profile(user_id=org_admin_b.id, track_id=track_ind.id)
    p_plat = Profile(user_id=plat_admin.id, track_id=track_gov.id)

    db_session.add_all([p_gov, p_ind, p_acad, p_admin_a, p_admin_b, p_plat])

    # Competency Frameworks & Competencies
    fw_gov = CompetencyFramework(track_id=track_gov.id, name="MoSPI Standards")
    fw_ind = CompetencyFramework(track_id=track_ind.id, name="Industry Analytics")
    fw_acad = CompetencyFramework(track_id=track_acad.id, name="Academic Foundation")
    db_session.add_all([fw_gov, fw_ind, fw_acad])
    db_session.flush()

    comp_gov = Competency(framework_id=fw_gov.id, code="GOV-STAT-01", name="Official Survey Design", category="Statistical", description="Gov Survey")
    comp_ind = Competency(framework_id=fw_ind.id, code="IND-SQL-01", name="Advanced SQL", category="Technical", description="Industry SQL")
    comp_acad = Competency(framework_id=fw_acad.id, code="ACAD-MATH-01", name="Discrete Math", category="Academic", description="Academia Math")
    db_session.add_all([comp_gov, comp_ind, comp_acad])

    # Documents
    doc_gov = Document(user_id=gov_user.id, organization_id=org_gov.id, filename="gov_confidential.pdf", mime_type="application/pdf", storage_key="/mock/gov", sha256="gov123", status="indexed")
    doc_ind = Document(user_id=ind_user.id, organization_id=org_ind_a.id, filename="industry_secrets.pdf", mime_type="application/pdf", storage_key="/mock/ind", sha256="ind123", status="indexed")
    doc_acad = Document(user_id=acad_user.id, organization_id=org_acad.id, filename="thesis_draft.pdf", mime_type="application/pdf", storage_key="/mock/acad", sha256="acad123", status="indexed")
    db_session.add_all([doc_gov, doc_ind, doc_acad])
    db_session.flush()

    # Document chunk for Gov
    chunk_gov = DocumentChunk(document_id=doc_gov.id, chunk_index=0, content="Official NSS round sampling methodology", embedding=[0.1]*768)
    # Document chunk for Ind
    chunk_ind = DocumentChunk(document_id=doc_ind.id, chunk_index=0, content="Proprietary revenue attribution model", embedding=[0.1]*768)
    db_session.add_all([chunk_gov, chunk_ind])

    db_session.commit()

    return {
        "gov_user": gov_user,
        "ind_user": ind_user,
        "acad_user": acad_user,
        "org_admin_a": org_admin_a,
        "org_admin_b": org_admin_b,
        "plat_admin": plat_admin,
        "org_gov": org_gov,
        "org_ind_a": org_ind_a,
        "org_ind_b": org_ind_b,
        "comp_gov": comp_gov,
        "comp_ind": comp_ind,
        "doc_gov": doc_gov,
        "doc_ind": doc_ind,
        "doc_acad": doc_acad,
        "fw_gov": fw_gov
    }


def test_1_academic_cannot_access_industry_records(client, test_setup):
    """1. Test that Academic user cannot access Industry document records."""
    token = create_access_token(test_setup["acad_user"].id)
    headers = {"Authorization": f"Bearer {token}"}

    # Academic tries to access Industry document details
    res = client.get(f"/api/v1/documents/{test_setup['doc_ind'].id}", headers=headers)
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


def test_2_industry_cannot_access_government_records(client, test_setup):
    """2. Test that Industry user cannot access Government document records."""
    token = create_access_token(test_setup["ind_user"].id)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get(f"/api/v1/documents/{test_setup['doc_gov'].id}", headers=headers)
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


def test_3_government_cannot_access_academic_private_records(client, test_setup):
    """3. Test that Government user cannot access Academic private documents."""
    token = create_access_token(test_setup["gov_user"].id)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get(f"/api/v1/documents/{test_setup['doc_acad'].id}", headers=headers)
    assert res.status_code == 403
    assert "forbidden" in res.json()["detail"].lower()


def test_4_org_admin_cannot_cross_organizations(client, test_setup):
    """4. Test that Organization Admin A cannot access Organization B analytics."""
    token_a = create_access_token(test_setup["org_admin_a"].id)
    headers = {"Authorization": f"Bearer {token_a}"}

    # Querying Org B while belonging to Org A -> 403 Forbidden
    res = client.get(f"/api/v1/analytics/org?organization_id={test_setup['org_ind_b'].id}", headers=headers)
    assert res.status_code == 403
    assert "cannot access another organization" in res.json()["detail"].lower()

    # Querying own organization -> 200 OK
    res_own = client.get(f"/api/v1/analytics/org?organization_id={test_setup['org_ind_a'].id}", headers=headers)
    assert res_own.status_code == 200
    assert res_own.json()["organization_id"] == test_setup["org_ind_a"].id


def test_5_platform_admin_can_access_authorized_global_analytics(client, test_setup):
    """5. Test that Platform Admin can access authorized global analytics and audit logs."""
    token = create_access_token(test_setup["plat_admin"].id)
    headers = {"Authorization": f"Bearer {token}"}

    # Access platform analytics
    res = client.get("/api/v1/analytics/platform", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["data_isolation_enforced"] is True
    assert "total_users" in data
    assert data["total_users"] >= 6

    # Access audit logs
    res_audit = client.get("/api/v1/admin/audit-events", headers=headers)
    assert res_audit.status_code == 200

    # Non-platform admin receives 403 on audit logs
    acad_token = create_access_token(test_setup["acad_user"].id)
    res_forbidden = client.get("/api/v1/admin/audit-events", headers={"Authorization": f"Bearer {acad_token}"})
    assert res_forbidden.status_code == 403


def test_6_ai_cannot_retrieve_unauthorized_documents(db_session, test_setup):
    """6. Test that AI assistant strictly scopes retrieval to caller's authorized documents."""
    # Academic user queries AI with terms from Government confidential document
    res = answer_assistant_query(
        db=db_session,
        user_id=test_setup["acad_user"].id,
        conversation_id="conv-1",
        message="What is the official NSS round sampling methodology?"
    )
    # Citations must not contain gov_confidential.pdf
    citation_docs = [c["document_title"] for c in res["citations"]]
    assert "gov_confidential.pdf" not in citation_docs


def test_7_dashboard_metrics_match_database_records(client, db_session, test_setup):
    """7. Test that /analytics/me dashboard metrics match actual database records."""
    user = test_setup["gov_user"]
    comp = test_setup["comp_gov"]

    # Seed 1 competency and 1 gap
    db_session.add(UserCompetency(
        user_id=user.id,
        competency_id=comp.id,
        score=75.0,
        proficiency_level=4,
        confidence=0.85,
        source="diagnostic"
    ))
    db_session.add(SkillGap(
        user_id=user.id,
        competency_id=comp.id,
        required_level=4,
        current_score=75.0,
        gap_value=5.0,
        priority="LOW",
        status="OPEN"
    ))
    db_session.commit()

    token = create_access_token(user.id)
    res = client.get("/api/v1/analytics/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    assert data["has_completed_diagnostic"] is True
    assert data["overall_score"] == 75.0
    assert data["total_competencies_tracked"] == 1
    assert data["open_gaps_count"] == 1
    assert data["radar_data"][0]["code"] == "GOV-STAT-01"
    assert data["radar_data"][0]["score"] == 75.0


def test_8_radar_values_match_competency_records(client, db_session, test_setup):
    """8. Test that competency radar values directly reflect current UserCompetency database state."""
    user = test_setup["ind_user"]
    comp = test_setup["comp_ind"]

    ucomp = UserCompetency(
        user_id=user.id,
        competency_id=comp.id,
        score=58.5,
        proficiency_level=3,
        confidence=0.72,
        source="quiz"
    )
    db_session.add(ucomp)
    db_session.commit()

    token = create_access_token(user.id)
    res = client.get("/api/v1/analytics/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()
    radar = data["radar_data"]
    assert len(radar) == 1
    assert radar[0]["code"] == "IND-SQL-01"
    assert radar[0]["score"] == 58.5


def test_9_assessment_quiz_changes_competency_when_configured(db_session, test_setup):
    """9. Test that quiz explicitly configured with is_competency_assessment=True updates competency and history."""
    user = test_setup["ind_user"]
    comp = test_setup["comp_ind"]

    quiz = Quiz(
        owner_id=user.id,
        title="Competency Assessment Quiz: SQL",
        competency_id=comp.id,
        is_competency_assessment=True,
        status="ready"
    )
    db_session.add(quiz)
    db_session.flush()

    q1 = QuizQuestion(
        quiz_id=quiz.id,
        prompt="What does SQL stand for?",
        options_json=["A", "B", "Structured Query Language", "D"],
        correct_option=2,
        explanation="Standard definition",
        source_ref="SQL Handbook"
    )
    db_session.add(q1)
    db_session.flush()

    attempt = QuizAttempt(quiz_id=quiz.id, user_id=user.id, score=0.0)
    db_session.add(attempt)
    db_session.commit()

    # Submit quiz with correct answer
    res = score_quiz_submission(
        db=db_session,
        attempt_id=attempt.id,
        user_id=user.id,
        answers={q1.id: 2}
    )

    assert res["score"] == 100.0
    impact = res["competency_impact"]
    assert impact["is_competency_assessment"] is True
    assert impact["new_score"] > impact["previous_score"]
    assert impact["delta"] > 0

    # Verify CompetencyHistory record was persisted in database
    history = db_session.query(CompetencyHistory).filter(CompetencyHistory.quiz_attempt_id == attempt.id).first()
    assert history is not None
    assert history.user_id == user.id
    assert history.competency_id == comp.id
    assert history.delta == impact["delta"]
    assert history.score_after == impact["new_score"]


def test_10_informational_quiz_does_not_alter_competency(db_session, test_setup):
    """10. Test that informational quiz (is_competency_assessment=False) does not alter competency or gap."""
    user = test_setup["gov_user"]
    comp = test_setup["comp_gov"]

    # Initial competency score
    ucomp = UserCompetency(user_id=user.id, competency_id=comp.id, score=60.0, proficiency_level=3, confidence=0.7)
    db_session.add(ucomp)
    db_session.commit()

    # Informational quiz
    quiz = Quiz(
        owner_id=user.id,
        title="Informational Quiz: Overview",
        competency_id=comp.id,
        is_competency_assessment=False,
        status="ready"
    )
    db_session.add(quiz)
    db_session.flush()

    q = QuizQuestion(
        quiz_id=quiz.id,
        prompt="Sample Informational Question",
        options_json=["A", "B", "C", "D"],
        correct_option=0,
        explanation="Explain",
        source_ref="Doc"
    )
    db_session.add(q)
    db_session.flush()

    attempt = QuizAttempt(quiz_id=quiz.id, user_id=user.id, score=0.0)
    db_session.add(attempt)
    db_session.commit()

    res = score_quiz_submission(db=db_session, attempt_id=attempt.id, user_id=user.id, answers={q.id: 0})
    assert res["score"] == 100.0
    assert res["competency_impact"]["is_competency_assessment"] is False

    # Check that UserCompetency score is strictly unchanged at 60.0
    db_session.refresh(ucomp)
    assert ucomp.score == 60.0

    # Check that no CompetencyHistory was created for this informational quiz
    h_count = db_session.query(CompetencyHistory).filter(CompetencyHistory.quiz_attempt_id == attempt.id).count()
    assert h_count == 0


def test_11_skill_gaps_recalculate_after_assessment(db_session, test_setup):
    """11. Test that skill gaps recalculate and CompetencyHistory is persisted during diagnostic assessment."""
    user = test_setup["acad_user"]
    fw = CompetencyFramework(track_id=test_setup["fw_gov"].track_id, name="Diagnostic FW")
    db_session.add(fw)
    db_session.flush()

    comp = Competency(framework_id=fw.id, code="DIAG-01", name="Diagnostic Skill", category="Core", description="Diag")
    db_session.add(comp)
    db_session.flush()

    assessment = Assessment(framework_id=fw.id, type="DIAGNOSTIC", title="Baseline Diagnostic")
    db_session.add(assessment)
    db_session.flush()

    aq = AssessmentQuestion(
        assessment_id=assessment.id,
        competency_id=comp.id,
        prompt="Test question",
        options_json=["A", "B", "C", "D"],
        answer_json=1,
        source_ref="Ref"
    )
    db_session.add(aq)
    db_session.flush()

    attempt = AssessmentAttempt(assessment_id=assessment.id, user_id=user.id, score=0.0)
    db_session.add(attempt)
    db_session.commit()

    # Score attempt: correct answer selected
    from app.models.assessment import AttemptAnswer
    db_session.add(AttemptAnswer(attempt_id=attempt.id, question_id=aq.id, selected_answer="1", is_correct=True))
    db_session.commit()

    score_assessment_attempt(db_session, attempt.id, user.id)

    # Verify SkillGap exists and is updated
    gap = db_session.query(SkillGap).filter(SkillGap.user_id == user.id, SkillGap.competency_id == comp.id).first()
    assert gap is not None
    assert gap.current_score == 100.0
    assert gap.gap_value == 0.0
    assert gap.status == "RESOLVED"

    # Verify CompetencyHistory
    history = db_session.query(CompetencyHistory).filter(
        CompetencyHistory.assessment_attempt_id == attempt.id,
        CompetencyHistory.competency_id == comp.id
    ).first()
    assert history is not None
    assert history.score_after == 100.0
    assert history.delta == 100.0


def test_12_public_overview_and_admin_security_enforcement(client, test_setup):
    """12. Test that public root works and non-admin cannot access admin users directory."""
    # Public root
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "STAT-SKILL AI" in res_root.json()["product"]

    # Non-admin user tries to access /admin/users
    ind_token = create_access_token(test_setup["ind_user"].id)
    res_users = client.get("/api/v1/admin/users", headers={"Authorization": f"Bearer {ind_token}"})
    assert res_users.status_code == 403
    assert "restricted to platform administrator" in res_users.json()["detail"].lower()
