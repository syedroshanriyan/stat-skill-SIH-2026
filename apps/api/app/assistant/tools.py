from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.models.competency import UserCompetency, Competency
from app.models.gap import SkillGap
from app.models.recommendation import LearningResource, ResourceCompetency
from app.models.learning_path import LearningPath
from app.models.assessment import AssessmentAttempt


def tool_get_profile(db: Session, user_id: str) -> Dict[str, Any]:
    user = db.query(User).filter(User.id == user_id).first()
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    return {
        "email": user.email if user else "",
        "display_name": user.display_name if user else "",
        "track": profile.track.code if profile and profile.track else "GOVERNMENT",
        "designation": profile.designation if profile else None,
        "department": profile.department if profile else None,
        "career_goal": profile.career_goal if profile else None
    }


def tool_get_competencies(db: Session, user_id: str) -> List[Dict[str, Any]]:
    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()
    return [
        {
            "code": uc.competency.code if uc.competency else "",
            "name": uc.competency.name if uc.competency else "",
            "category": uc.competency.category if uc.competency else "",
            "score": uc.score,
            "proficiency_level": uc.proficiency_level
        }
        for uc in user_comps
    ]


def tool_get_skill_gaps(db: Session, user_id: str) -> List[Dict[str, Any]]:
    gaps = db.query(SkillGap).filter(SkillGap.user_id == user_id).all()
    return [
        {
            "code": g.competency.code if g.competency else "",
            "name": g.competency.name if g.competency else "",
            "required_level": g.required_level,
            "current_score": g.current_score,
            "gap_value": g.gap_value,
            "priority": g.priority,
            "status": g.status
        }
        for g in gaps
    ]


def tool_search_resources(db: Session, query: Optional[str] = None, provider: Optional[str] = None) -> List[Dict[str, Any]]:
    q = db.query(LearningResource)
    if provider:
        q = q.filter(LearningResource.provider_type == provider.lower())
    if query:
        q = q.filter(LearningResource.title.ilike(f"%{query}%") | LearningResource.description.ilike(f"%{query}%"))
    resources = q.limit(5).all()
    return [
        {
            "id": r.id,
            "provider": r.provider_type,
            "external_id": r.provider_external_id,
            "title": r.title,
            "level": r.level,
            "duration": r.duration,
            "url": r.url
        }
        for r in resources
    ]


def tool_get_learning_path(db: Session, user_id: str) -> Dict[str, Any]:
    path = db.query(LearningPath).filter(LearningPath.user_id == user_id, LearningPath.status == "active").first()
    if not path:
        return {"has_active_path": False}
    return {
        "has_active_path": True,
        "title": path.title,
        "goal": path.goal,
        "items_count": len(path.items),
        "items": [
            {
                "sequence": item.sequence,
                "title": item.resource.title if item.resource else "Resource",
                "provider": item.resource.provider_type if item.resource else "",
                "status": item.status
            }
            for item in path.items
        ]
    }


def tool_get_assessment_results(db: Session, user_id: str) -> List[Dict[str, Any]]:
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == user_id)
        .order_by(AssessmentAttempt.started_at.desc())
        .limit(3)
        .all()
    )
    return [
        {
            "attempt_id": a.id,
            "assessment_title": a.assessment.title if a.assessment else "",
            "score": a.score,
            "completed_at": a.completed_at.isoformat() if a.completed_at else None
        }
        for a in attempts
    ]
