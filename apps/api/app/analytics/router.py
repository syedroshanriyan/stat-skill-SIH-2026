from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.auth.deps import get_current_user, get_auth_context, AuthContext, require_platform_admin
from app.models.user import User, Profile, Membership, Organization, Track
from app.models.competency import UserCompetency, Competency, RoleCompetency
from app.models.gap import SkillGap
from app.models.assessment import AssessmentAttempt
from app.models.quiz import QuizAttempt
from app.models.evidence import Evidence
from app.models.learning_path import LearningPath, LearningPathItem

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/me")
def get_learner_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # 1. Competency Radar by Category (Real Database Records)
    user_comps = (
        db.query(UserCompetency)
        .filter(UserCompetency.user_id == current_user.id)
        .join(Competency)
        .all()
    )

    categories: Dict[str, List[float]] = {}
    radar_data = []

    for uc in user_comps:
        cat = uc.competency.category if uc.competency else "General"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(uc.score)

        radar_data.append({
            "code": uc.competency.code if uc.competency else "",
            "name": uc.competency.name if uc.competency else "",
            "category": cat,
            "score": round(uc.score, 1),
            "level": uc.proficiency_level,
            "required_level": 3
        })

    category_averages = {
        cat: round(sum(scores) / len(scores), 1)
        for cat, scores in categories.items()
    }

    # 2. Skill Gaps Summary
    gaps = db.query(SkillGap).filter(SkillGap.user_id == current_user.id).all()
    open_gaps = [g for g in gaps if g.status == "OPEN"]
    critical_gaps = [g for g in open_gaps if g.priority == "CRITICAL"]

    # 3. Learning Progress
    path = db.query(LearningPath).filter(LearningPath.user_id == current_user.id, LearningPath.status == "active").first()
    total_steps = len(path.items) if path else 0
    completed_steps = len([i for i in path.items if i.status == "completed"]) if path else 0
    progress_pct = round((completed_steps / total_steps * 100.0) if total_steps > 0 else 0.0, 1)

    # 4. Assessments Summary
    attempts = db.query(AssessmentAttempt).filter(AssessmentAttempt.user_id == current_user.id).all()
    total_attempts = len(attempts)
    avg_score = round(sum(a.score for a in attempts) / total_attempts, 1) if total_attempts > 0 else 0.0

    # 5. Quiz Performance (Real Aggregation)
    quiz_attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    total_quizzes = len(quiz_attempts)
    avg_quiz_score = round(sum(q.score for q in quiz_attempts) / total_quizzes, 1) if total_quizzes > 0 else 0.0

    # 6. Evidence
    evidence_items = db.query(Evidence).filter(Evidence.user_id == current_user.id).all()

    # Determine if user has established their baseline
    has_completed_diagnostic = bool(total_attempts > 0 or len(user_comps) > 0)

    return {
        "has_completed_diagnostic": has_completed_diagnostic,
        "overall_score": round(sum(uc.score for uc in user_comps) / len(user_comps), 1) if user_comps else 0.0,
        "radar_data": radar_data,
        "category_averages": category_averages,
        "total_competencies_tracked": len(user_comps),
        "open_gaps_count": len(open_gaps),
        "critical_gaps_count": len(critical_gaps),
        "learning_progress_pct": progress_pct,
        "completed_learning_steps": completed_steps,
        "total_learning_steps": total_steps,
        "assessment_attempts_count": total_attempts,
        "average_assessment_score": avg_score,
        "total_quizzes_taken": total_quizzes,
        "average_quiz_score": avg_quiz_score,
        "evidence_count": len(evidence_items)
    }


def _get_authorized_org_user_ids(auth: AuthContext, db: Session, target_org_id: Optional[str] = None) -> List[str]:
    """Helper to return user IDs strictly within the caller's authorized organization scope."""
    if auth.is_platform_admin:
        if target_org_id:
            memberships = db.query(Membership).filter(Membership.organization_id == target_org_id).all()
            return [m.user_id for m in memberships]
        memberships = db.query(Membership).all()
        return [m.user_id for m in memberships] or [auth.user.id]

    # Non-platform admin: Must be org_admin or institution_admin
    allowed_admin_roles = ["org_admin", "institution_admin"]
    if not any(r in allowed_admin_roles for r in auth.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Organization analytics require org_admin or institution_admin privileges"
        )

    # Must stay within caller's own organization
    if target_org_id and target_org_id not in auth.organization_ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Organization Admin cannot access another organization's records"
        )

    org_id = target_org_id or (auth.organization_ids[0] if auth.organization_ids else None)
    if not org_id:
        return [auth.user.id]

    memberships = db.query(Membership).filter(Membership.organization_id == org_id).all()
    return [m.user_id for m in memberships] or [auth.user.id]


@router.get("/org")
def get_organization_analytics(
    organization_id: Optional[str] = Query(None),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    user_ids = _get_authorized_org_user_ids(auth, db, organization_id)
    target_org_id = organization_id or (auth.organization_ids[0] if auth.organization_ids else None)
    org = db.query(Organization).filter(Organization.id == target_org_id).first() if target_org_id else None

    # Workforce average score from real database records
    all_scores = db.query(UserCompetency.score).filter(UserCompetency.user_id.in_(user_ids)).all()
    workforce_avg = round(sum(s[0] for s in all_scores) / len(all_scores), 1) if all_scores else 0.0

    # Proficiency level distribution
    levels = db.query(UserCompetency.proficiency_level, func.count(UserCompetency.id)).filter(
        UserCompetency.user_id.in_(user_ids)
    ).group_by(UserCompetency.proficiency_level).all()
    level_dist = {f"Level {lvl}": count for lvl, count in levels}

    # Top organization training demands
    top_gaps = (
        db.query(Competency.name, Competency.code, func.count(SkillGap.id), func.avg(SkillGap.gap_value))
        .join(SkillGap, SkillGap.competency_id == Competency.id)
        .filter(SkillGap.user_id.in_(user_ids), SkillGap.status == "OPEN")
        .group_by(Competency.name, Competency.code)
        .order_by(func.count(SkillGap.id).desc())
        .limit(5)
        .all()
    )

    training_demand = [
        {
            "code": code,
            "competency": name,
            "headcount_needing_training": count,
            "average_gap": round(float(avg_gap), 1)
        }
        for name, code, count, avg_gap in top_gaps
    ]

    return {
        "organization_id": org.id if org else None,
        "organization_name": org.name if org else "Authorized Scope",
        "organization_type": org.type if org else auth.track_code,
        "total_staff_enrolled": len(user_ids),
        "workforce_average_competency": workforce_avg,
        "proficiency_distribution": level_dist,
        "top_training_demands": training_demand
    }


@router.get("/org/competencies")
def get_org_competencies_matrix(
    organization_id: Optional[str] = Query(None),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
):
    user_ids = _get_authorized_org_user_ids(auth, db, organization_id)
    comps = db.query(Competency).order_by(Competency.category, Competency.code).all()
    results = []
    for c in comps:
        avg_score = (
            db.query(func.avg(UserCompetency.score))
            .filter(UserCompetency.competency_id == c.id, UserCompetency.user_id.in_(user_ids))
            .scalar() or 0.0
        )
        active_learners = (
            db.query(func.count(UserCompetency.id))
            .filter(UserCompetency.competency_id == c.id, UserCompetency.user_id.in_(user_ids))
            .scalar() or 0
        )
        results.append({
            "code": c.code,
            "name": c.name,
            "category": c.category,
            "average_score": round(float(avg_score), 1),
            "assessed_learners": active_learners
        })
    return results


@router.get("/org/gaps")
def get_org_gaps_heatmap(
    organization_id: Optional[str] = Query(None),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
):
    user_ids = _get_authorized_org_user_ids(auth, db, organization_id)
    gaps = (
        db.query(Competency.category, SkillGap.priority, func.count(SkillGap.id))
        .join(Competency, SkillGap.competency_id == Competency.id)
        .filter(SkillGap.status == "OPEN", SkillGap.user_id.in_(user_ids))
        .group_by(Competency.category, SkillGap.priority)
        .all()
    )
    return [
        {"category": cat, "priority": prio, "count": cnt}
        for cat, prio, cnt in gaps
    ]


@router.get("/org/training-demand")
def get_org_training_demand(
    organization_id: Optional[str] = Query(None),
    auth: AuthContext = Depends(get_auth_context),
    db: Session = Depends(get_db)
):
    user_ids = _get_authorized_org_user_ids(auth, db, organization_id)
    top_demands = (
        db.query(Competency.name, Competency.category, func.count(SkillGap.id), func.avg(SkillGap.gap_value))
        .join(SkillGap, SkillGap.competency_id == Competency.id)
        .filter(SkillGap.status == "OPEN", SkillGap.user_id.in_(user_ids))
        .group_by(Competency.name, Competency.category)
        .order_by(func.count(SkillGap.id).desc())
        .limit(10)
        .all()
    )
    return [
        {
            "competency": name,
            "category": cat,
            "demand_count": count,
            "average_gap": round(float(avg_gap), 1)
        }
        for name, cat, count, avg_gap in top_demands
    ]


@router.get("/platform")
def get_platform_global_analytics(
    current_user: User = Depends(require_platform_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Dedicated Platform-Admin-Only analytics endpoint providing global, authorized platform metrics."""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.status == "active").count()
    total_orgs = db.query(Organization).count()
    total_competencies = db.query(Competency).count()
    total_attempts = db.query(AssessmentAttempt).count()
    total_quizzes = db.query(QuizAttempt).count()
    total_gaps = db.query(SkillGap).filter(SkillGap.status == "OPEN").count()

    all_scores = db.query(UserCompetency.score).all()
    global_avg_competency = round(sum(s[0] for s in all_scores) / len(all_scores), 1) if all_scores else 0.0

    # User count per track
    tracks = db.query(Track).all()
    track_distribution = {}
    for t in tracks:
        cnt = db.query(Profile).filter(Profile.track_id == t.id).count()
        track_distribution[t.code] = cnt

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_organizations": total_orgs,
        "total_competencies": total_competencies,
        "total_assessment_attempts": total_attempts,
        "total_quizzes_completed": total_quizzes,
        "total_active_skill_gaps": total_gaps,
        "global_average_competency": global_avg_competency,
        "track_distribution": track_distribution,
        "data_isolation_enforced": True
    }
