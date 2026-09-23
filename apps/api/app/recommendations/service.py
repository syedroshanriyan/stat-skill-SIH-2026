from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session
from app.models.user import User, Profile
from app.models.gap import SkillGap
from app.models.competency import Competency
from app.models.recommendation import LearningResource, ResourceCompetency, Recommendation


def generate_hybrid_recommendations(db: Session, user_id: str) -> List[Recommendation]:
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    track_code = profile.track.code if profile and profile.track else "GOVERNMENT"

    # Get open skill gaps for user sorted by priority
    gaps = (
        db.query(SkillGap)
        .filter(SkillGap.user_id == user_id, SkillGap.status == "OPEN")
        .order_by(SkillGap.gap_value.desc())
        .all()
    )

    if not gaps:
        return db.query(Recommendation).filter(Recommendation.user_id == user_id).all()

    # Map target providers based on track
    preferred_providers = ["igot", "nssta"] if track_code == "GOVERNMENT" else (
        ["industry"] if track_code == "INDUSTRY" else ["academia"]
    )

    rank_counter = 1
    for gap in gaps:
        # Find matching resources mapped to this competency
        resource_mappings = (
            db.query(ResourceCompetency)
            .filter(ResourceCompetency.competency_id == gap.competency_id)
            .join(LearningResource)
            .all()
        )

        for rm in resource_mappings:
            res = rm.resource
            if not res:
                continue

            # Calculate hybrid score
            # Base gap score (0-100) * 0.4
            gap_weight = min(1.0, gap.gap_value / 50.0) * 40.0
            # Relevance score * 30
            rel_weight = rm.relevance_score * 30.0
            # Track preference * 20
            provider_weight = 20.0 if res.provider_type in preferred_providers else 10.0
            # Priority bonus * 10
            priority_weight = 10.0 if gap.priority in ["CRITICAL", "HIGH"] else 5.0

            total_score = round(gap_weight + rel_weight + provider_weight + priority_weight, 1)

            provider_label = "iGOT Karmayogi" if res.provider_type == "igot" else (
                "NSSTA TPAC" if res.provider_type == "nssta" else (
                    "Industry Standard" if res.provider_type == "industry" else "University Course"
                )
            )

            explanation = (
                f"Recommended by {provider_label} to close high-priority gap in "
                f"{gap.competency.name if gap.competency else 'target area'} (Gap: {gap.gap_value:.0f} pts). "
                f"Expected outcome: Elevates proficiency toward Level {gap.required_level}."
            )

            # Check if recommendation already exists
            existing_rec = db.query(Recommendation).filter(
                Recommendation.user_id == user_id,
                Recommendation.resource_id == res.id,
                Recommendation.competency_id == gap.competency_id
            ).first()

            if existing_rec:
                existing_rec.score = total_score
                existing_rec.rank = rank_counter
                existing_rec.explanation = explanation
            else:
                new_rec = Recommendation(
                    user_id=user_id,
                    resource_id=res.id,
                    competency_id=gap.competency_id,
                    rank=rank_counter,
                    score=total_score,
                    explanation=explanation,
                    status="suggested"
                )
                db.add(new_rec)

            rank_counter += 1

    db.commit()
    return (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user_id)
        .order_by(Recommendation.score.desc())
        .all()
    )
