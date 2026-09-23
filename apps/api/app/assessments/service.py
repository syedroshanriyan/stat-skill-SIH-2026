from datetime import datetime, timezone
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, AttemptAnswer
from app.models.competency import Competency, UserCompetency, CompetencyFramework
from app.models.competency_history import CompetencyHistory
from app.models.gap import SkillGap
from app.models.audit import AuditEvent


def score_assessment_attempt(db: Session, attempt_id: str, user_id: str) -> Dict[str, Any]:
    attempt = db.query(AssessmentAttempt).filter(
        AssessmentAttempt.id == attempt_id,
        AssessmentAttempt.user_id == user_id
    ).first()
    if not attempt:
        raise ValueError("Assessment attempt not found")

    answers = db.query(AttemptAnswer).filter(AttemptAnswer.attempt_id == attempt_id).all()
    questions = (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.assessment_id == attempt.assessment_id)
        .all()
    )

    question_map = {q.id: q for q in questions}
    total_questions = len(questions)
    correct_count = 0

    # Competency breakdown: {comp_id: {"total": int, "correct": int, "name": str, "code": str}}
    comp_breakdown: Dict[str, Dict[str, Any]] = {}

    for q in questions:
        cid = q.competency_id
        if cid not in comp_breakdown:
            comp_breakdown[cid] = {
                "total": 0,
                "correct": 0,
                "code": q.competency.code if q.competency else "UNKNOWN",
                "name": q.competency.name if q.competency else "Competency",
            }
        comp_breakdown[cid]["total"] += 1

    for ans in answers:
        q = question_map.get(ans.question_id)
        if not q:
            continue
        # ans.selected_answer vs q.answer_json
        is_correct = False
        try:
            is_correct = int(ans.selected_answer) == int(q.answer_json)
        except (ValueError, TypeError):
            is_correct = str(ans.selected_answer).strip() == str(q.answer_json).strip()

        ans.is_correct = is_correct
        if is_correct:
            correct_count += 1
            if q.competency_id in comp_breakdown:
                comp_breakdown[q.competency_id]["correct"] += 1

    overall_score = (correct_count / total_questions * 100.0) if total_questions > 0 else 0.0
    attempt.score = round(overall_score, 1)
    attempt.completed_at = datetime.now(timezone.utc)

    # Deterministic Competency Updates & Skill Gap recalculation
    evolution = []
    largest_imp = None
    max_delta = -999.0
    highest_score = -1.0
    strongest_comp = None

    for comp_id, stats in comp_breakdown.items():
        comp_score = (stats["correct"] / stats["total"] * 100.0) if stats["total"] > 0 else 0.0
        # Calculate proficiency level: 0-20: 1, 21-40: 2, 41-60: 3, 61-80: 4, 81-100: 5
        level = max(1, min(5, int(comp_score // 20) + 1))
        confidence = 0.85 if stats["total"] >= 2 else 0.70

        user_comp = db.query(UserCompetency).filter(
            UserCompetency.user_id == user_id,
            UserCompetency.competency_id == comp_id
        ).first()

        prev_score = user_comp.score if user_comp else 0.0
        prev_conf = user_comp.confidence if user_comp else 0.5

        if user_comp:
            # Weighted update: 60% new assessment + 40% prior score
            blended_score = round(user_comp.score * 0.4 + comp_score * 0.6, 1)
            user_comp.score = blended_score
            user_comp.proficiency_level = max(1, min(5, int(blended_score // 20) + 1))
            user_comp.confidence = min(0.95, round(user_comp.confidence + 0.05, 2))
            user_comp.source = "diagnostic"
            user_comp.assessed_at = datetime.now(timezone.utc)
            user_comp.version += 1
        else:
            user_comp = UserCompetency(
                user_id=user_id,
                competency_id=comp_id,
                score=round(comp_score, 1),
                proficiency_level=level,
                confidence=confidence,
                source="diagnostic",
                version=1
            )
            db.add(user_comp)

        # Persist CompetencyHistory snapshot with deterministic delta
        delta = round(user_comp.score - prev_score, 1)
        db.add(CompetencyHistory(
            user_id=user_id,
            competency_id=comp_id,
            assessment_attempt_id=attempt_id,
            score_before=prev_score,
            score_after=user_comp.score,
            delta=delta,
            confidence_before=prev_conf,
            confidence_after=user_comp.confidence,
            source="diagnostic",
            timestamp=datetime.now(timezone.utc)
        ))

        # Update or create skill gap against standard level 3 (or 4 for core)
        gap = db.query(SkillGap).filter(
            SkillGap.user_id == user_id,
            SkillGap.competency_id == comp_id
        ).first()

        req_level = gap.required_level if gap else 3
        req_score = req_level * 20.0
        final_score = user_comp.score
        gap_val = max(0.0, req_score - final_score)
        priority = "CRITICAL" if gap_val >= 35.0 else ("HIGH" if gap_val >= 20.0 else ("MEDIUM" if gap_val > 0 else "LOW"))
        status_val = "RESOLVED" if gap_val == 0 else "OPEN"

        if gap:
            gap.current_score = final_score
            gap.gap_value = gap_val
            gap.priority = priority
            gap.status = status_val
            gap.explanation = f"Assessment completed with {comp_score:.0f}% performance. Target level: {req_level} ({req_score:.0f} pts)."
        else:
            db.add(SkillGap(
                user_id=user_id,
                competency_id=comp_id,
                required_level=req_level,
                current_score=final_score,
                gap_value=gap_val,
                priority=priority,
                status=status_val,
                explanation=f"Baseline established from assessment: {comp_score:.0f}% score."
            ))

        evolution.append({
            "competency_id": comp_id,
            "code": stats["code"],
            "name": stats["name"],
            "score_before": prev_score,
            "score_after": user_comp.score,
            "delta": delta,
            "confidence_before": prev_conf,
            "confidence_after": user_comp.confidence,
            "proficiency_level": user_comp.proficiency_level,
            "gap_value": gap_val,
            "is_resolved": status_val == "RESOLVED"
        })

        if delta > max_delta:
            max_delta = delta
            largest_imp = f"{stats['code']}: {stats['name']} (+{delta:.1f} pts)"

        if user_comp.score > highest_score:
            highest_score = user_comp.score
            strongest_comp = f"{stats['code']}: {stats['name']} ({user_comp.score:.1f} pts)"

    # Dynamically recompute hybrid recommendations based on updated state
    from app.recommendations.service import generate_hybrid_recommendations
    generate_hybrid_recommendations(db, user_id)

    # Count remaining and resolved gaps
    all_gaps = db.query(SkillGap).filter(SkillGap.user_id == user_id).all()
    remaining_gaps = len([g for g in all_gaps if g.status == "OPEN"])
    closed_gaps = len([g for g in all_gaps if g.status == "RESOLVED"])

    # Audit event
    db.add(AuditEvent(
        actor_id=user_id,
        action="ASSESSMENT_COMPLETED",
        entity_type="ASSESSMENT_ATTEMPT",
        entity_id=attempt_id,
        metadata_json={
            "score": attempt.score,
            "total_questions": total_questions,
            "correct": correct_count
        }
    ))

    db.commit()

    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "score": attempt.score,
        "total_questions": total_questions,
        "correct_answers": correct_count,
        "competency_breakdown": comp_breakdown,
        "competency_evolution": evolution,
        "strongest_area": strongest_comp or "Domain Knowledge",
        "largest_improvement": largest_imp or "Baseline Established",
        "remaining_gaps_count": remaining_gaps,
        "closed_gaps_count": closed_gaps,
        "recommendations_updated": True,
        "completed_at": attempt.completed_at
    }

