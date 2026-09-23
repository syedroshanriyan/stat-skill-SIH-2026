from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.user import User, Profile, Role
from app.models.competency import RoleCompetency, UserCompetency, Competency
from app.models.gap import SkillGap


def recalculate_user_skill_gaps(db: Session, user_id: str) -> List[SkillGap]:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    target_role_id = profile.target_role_id if profile else None

    # Fetch required competencies for role or default framework competencies
    role_competencies = []
    if target_role_id:
        role_competencies = db.query(RoleCompetency).filter(RoleCompetency.role_id == target_role_id).all()

    # User's current competencies map
    user_comps = db.query(UserCompetency).filter(UserCompetency.user_id == user_id).all()
    user_comp_map = {uc.competency_id: uc for uc in user_comps}

    # If role competencies exist, compare against them; otherwise against all competencies user has attempted
    evaluated_comp_ids = set()

    if role_competencies:
        for rc in role_competencies:
            evaluated_comp_ids.add(rc.competency_id)
            current_uc = user_comp_map.get(rc.competency_id)
            current_score = current_uc.score if current_uc else 0.0
            required_score = rc.required_level * 20.0
            gap_val = max(0.0, required_score - current_score)

            # Priority classification
            if gap_val >= 35.0 or rc.priority == "CRITICAL":
                priority = "CRITICAL"
            elif gap_val >= 20.0 or rc.priority == "HIGH":
                priority = "HIGH"
            elif gap_val > 0:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            status = "RESOLVED" if gap_val == 0 else "OPEN"
            explanation = (
                f"Role target is Level {rc.required_level} ({required_score:.0f} pts). "
                f"Current evaluated score is {current_score:.0f} pts (Gap: {gap_val:.0f} pts)."
            )

            gap = db.query(SkillGap).filter(
                SkillGap.user_id == user_id,
                SkillGap.competency_id == rc.competency_id
            ).first()

            if gap:
                gap.required_level = rc.required_level
                gap.current_score = current_score
                gap.gap_value = gap_val
                gap.priority = priority
                gap.status = status
                gap.explanation = explanation
                gap.updated_at = datetime.now(timezone.utc)
            else:
                gap = SkillGap(
                    user_id=user_id,
                    competency_id=rc.competency_id,
                    required_level=rc.required_level,
                    current_score=current_score,
                    gap_value=gap_val,
                    priority=priority,
                    status=status,
                    explanation=explanation
                )
                db.add(gap)

    # For any user competencies without explicit role requirement, assume standard level 3 benchmark
    for cid, uc in user_comp_map.items():
        if cid in evaluated_comp_ids:
            continue
        req_level = 3
        required_score = req_level * 20.0
        gap_val = max(0.0, required_score - uc.score)
        priority = "HIGH" if gap_val >= 25.0 else ("MEDIUM" if gap_val > 0 else "LOW")
        status = "RESOLVED" if gap_val == 0 else "OPEN"

        gap = db.query(SkillGap).filter(
            SkillGap.user_id == user_id,
            SkillGap.competency_id == cid
        ).first()

        if gap:
            gap.current_score = uc.score
            gap.gap_value = gap_val
            gap.priority = priority
            gap.status = status
            gap.updated_at = datetime.now(timezone.utc)
        else:
            db.add(SkillGap(
                user_id=user_id,
                competency_id=cid,
                required_level=req_level,
                current_score=uc.score,
                gap_value=gap_val,
                priority=priority,
                status=status,
                explanation=f"General baseline target level 3 ({required_score:.0f} pts)."
            ))

    db.commit()
    return db.query(SkillGap).filter(SkillGap.user_id == user_id).all()
