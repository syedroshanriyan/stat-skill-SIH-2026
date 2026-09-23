import pytest
from app.core.security import get_password_hash, create_access_token
from app.models.user import User, Track, Profile, Organization, Membership
from app.models.competency import CompetencyFramework, Competency, UserCompetency
from app.models.gap import SkillGap
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AttemptAnswer
from app.models.document import Document, DocumentChunk
from app.models.quiz import Quiz, QuizQuestion, QuizAttempt


def test_health_endpoints(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

    res_ready = client.get("/api/v1/ready")
    assert res_ready.status_code == 200
    assert "status" in res_ready.json()


def test_user_registration_and_login(client, db_session):
    # Register
    reg_payload = {
        "email": "test.official@mospi.gov.in",
        "password": "SecurePassword@123",
        "display_name": "Test Official",
        "track": "GOVERNMENT",
        "role": "official",
        "organization_name": "MoSPI Field Operations"
    }
    res = client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["email"] == "test.official@mospi.gov.in"
    assert data["track"] == "GOVERNMENT"

    # Login
    login_payload = {
        "email": "test.official@mospi.gov.in",
        "password": "SecurePassword@123"
    }
    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    token = res_login.json()["access_token"]
    assert token

    # Check /me
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/v1/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == "test.official@mospi.gov.in"


def test_skill_gap_deterministic_calculation(client, db_session):
    # Setup test track, user, framework, competency
    track = Track(code="TEST_GOV", name="Test Track")
    db_session.add(track)
    db_session.flush()

    user = User(
        email="gap.tester@mospi.gov.in",
        password_hash=get_password_hash("Password123"),
        display_name="Gap Tester"
    )
    db_session.add(user)
    db_session.flush()

    fw = CompetencyFramework(track_id=track.id, name="Test Framework")
    db_session.add(fw)
    db_session.flush()

    comp = Competency(
        framework_id=fw.id,
        code="STAT-TEST-01",
        name="Sampling Precision",
        category="Statistical",
        description="Testing sampling precision"
    )
    db_session.add(comp)
    db_session.flush()

    # User score 45.0 (Level 2), Target is 3 (Score 60.0) -> Gap = 15.0
    ucomp = UserCompetency(
        user_id=user.id,
        competency_id=comp.id,
        score=45.0,
        proficiency_level=2,
        confidence=0.8,
        source="diagnostic"
    )
    db_session.add(ucomp)
    db_session.commit()

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/api/v1/me/gaps", headers=headers)
    assert res.status_code == 200
    gaps = res.json()
    assert len(gaps) >= 1
    found_gap = next((g for g in gaps if g["competency_id"] == comp.id), None)
    assert found_gap is not None
    assert found_gap["gap_value"] == 15.0
    assert found_gap["required_level"] == 3
    assert found_gap["priority"] == "MEDIUM"


def test_assessment_attempt_and_scoring(client, db_session):
    track = Track(code="GOV_ASSESS", name="Government Track")
    db_session.add(track)
    db_session.flush()

    user = User(
        email="assessment.user@mospi.gov.in",
        password_hash=get_password_hash("Pass@123"),
        display_name="Assessment User"
    )
    db_session.add(user)
    db_session.flush()

    fw = CompetencyFramework(track_id=track.id, name="MoSPI Framework")
    db_session.add(fw)
    db_session.flush()

    comp = Competency(
        framework_id=fw.id,
        code="STAT-SURVEY-01",
        name="Survey Design",
        category="Statistical",
        description="Survey design competency"
    )
    db_session.add(comp)
    db_session.flush()

    assessment = Assessment(
        framework_id=fw.id,
        type="DIAGNOSTIC",
        title="Diagnostic Assessment 1"
    )
    db_session.add(assessment)
    db_session.flush()

    q1 = AssessmentQuestion(
        assessment_id=assessment.id,
        competency_id=comp.id,
        prompt="What is stratified sampling?",
        options_json=["Opt 0", "Opt 1", "Opt 2", "Opt 3"],
        answer_json=2
    )
    db_session.add(q1)
    db_session.commit()

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Start attempt
    res_start = client.post(f"/api/v1/assessments/{assessment.id}/attempts", headers=headers)
    assert res_start.status_code == 201
    attempt_id = res_start.json()["attempt_id"]

    # Record correct answer (option index 2)
    ans_payload = {"question_id": q1.id, "selected_answer": 2}
    res_ans = client.post(f"/api/v1/attempts/{attempt_id}/answers", json=ans_payload, headers=headers)
    assert res_ans.status_code == 200
    assert res_ans.json()["is_correct"] is True

    # Complete attempt
    res_comp = client.post(f"/api/v1/attempts/{attempt_id}/complete", headers=headers)
    assert res_comp.status_code == 200
    res_data = res_comp.json()
    assert res_data["score"] == 100.0
    assert res_data["correct_answers"] == 1


def test_quiz_generation_and_scoring(client, db_session):
    user = User(
        email="quiz.tester@mospi.gov.in",
        password_hash=get_password_hash("Pass@123"),
        display_name="Quiz Tester"
    )
    db_session.add(user)
    db_session.flush()

    track = Track(code="QUIZ_TRACK", name="Quiz Track")
    db_session.add(track)
    db_session.flush()

    fw = CompetencyFramework(track_id=track.id, name="Quiz Framework")
    db_session.add(fw)
    db_session.flush()

    comp = Competency(
        framework_id=fw.id,
        code="QUIZ-COMP-01",
        name="Sampling Variance",
        category="Statistical",
        description="Sampling variance description"
    )
    db_session.add(comp)
    db_session.flush()

    doc = Document(
        user_id=user.id,
        filename="survey_manual.pdf",
        mime_type="application/pdf",
        storage_key="test_path",
        sha256="fakehash123",
        status="indexed"
    )
    db_session.add(doc)
    db_session.flush()

    chunk = DocumentChunk(
        document_id=doc.id,
        chunk_index=0,
        content="Stratified sampling minimizes sampling variance when strata are homogeneous internally.",
        page_number=1,
        metadata_json={}
    )
    db_session.add(chunk)
    db_session.commit()

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Generate quiz
    gen_payload = {
        "source_document_id": doc.id,
        "competency_id": comp.id,
        "difficulty": "medium",
        "question_count": 2,
        "title": "Grounded Sampling Quiz"
    }
    res_gen = client.post("/api/v1/quizzes/generate", json=gen_payload, headers=headers)
    assert res_gen.status_code == 201
    quiz = res_gen.json()
    assert quiz["title"] == "Grounded Sampling Quiz"
    assert len(quiz["questions"]) == 2

    # Verify each question has exactly 4 options and valid correct index
    for q in quiz["questions"]:
        assert len(q["options_json"]) == 4

    # Start quiz attempt
    res_attempt = client.post(f"/api/v1/quizzes/{quiz['id']}/attempts", headers=headers)
    assert res_attempt.status_code == 201
    attempt_id = res_attempt.json()["attempt_id"]

    # Submit quiz answers
    q_id_1 = quiz["questions"][0]["id"]
    answers = {q_id_1: 0}
    res_sub = client.post(f"/api/v1/quiz-attempts/{attempt_id}/submit", json={"answers": answers}, headers=headers)
    assert res_sub.status_code == 200
    res_data = res_sub.json()
    assert "score" in res_data
    assert "competency_impact" in res_data
