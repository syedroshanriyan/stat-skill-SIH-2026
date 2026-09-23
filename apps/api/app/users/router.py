from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User, Profile, Membership, Track, Role
from app.models.audit import AuditEvent
from app.schemas.user import UserResponse, UserUpdate, ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/me", tags=["Users"])


@router.get("", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    membership = db.query(Membership).filter(Membership.user_id == current_user.id).first()

    track_code = None
    if profile and profile.track:
        track_code = profile.track.code

    role = membership.role if membership else "learner"

    profile_resp = None
    if profile:
        profile_resp = ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            track_id=profile.track_id,
            track_code=track_code,
            designation=profile.designation,
            department=profile.department,
            education_json=profile.education_json,
            experience_json=profile.experience_json,
            career_goal=profile.career_goal,
            target_role_id=profile.target_role_id,
            metadata_json=profile.metadata_json
        )

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        display_name=current_user.display_name,
        status=current_user.status,
        track_code=track_code,
        role=role,
        profile=profile_resp,
        created_at=current_user.created_at
    )


@router.patch("", response_model=UserResponse)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if payload.display_name:
        current_user.display_name = payload.display_name

    db.add(AuditEvent(
        actor_id=current_user.id,
        action="USER_UPDATE",
        entity_type="USER",
        entity_id=current_user.id,
        metadata_json={"display_name": current_user.display_name}
    ))
    db.commit()
    db.refresh(current_user)
    return get_me(current_user, db)


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    track_code = profile.track.code if profile.track else None
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        track_id=profile.track_id,
        track_code=track_code,
        designation=profile.designation,
        department=profile.department,
        education_json=profile.education_json,
        experience_json=profile.experience_json,
        career_goal=profile.career_goal,
        target_role_id=profile.target_role_id,
        metadata_json=profile.metadata_json
    )


@router.patch("/profile", response_model=ProfileResponse)
def update_profile(
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    if payload.designation is not None:
        profile.designation = payload.designation
    if payload.department is not None:
        profile.department = payload.department
    if payload.education_json is not None:
        profile.education_json = payload.education_json
    if payload.experience_json is not None:
        profile.experience_json = payload.experience_json
    if payload.career_goal is not None:
        profile.career_goal = payload.career_goal
    if payload.target_role_id is not None:
        profile.target_role_id = payload.target_role_id
    if payload.metadata_json is not None:
        profile.metadata_json = payload.metadata_json

    db.add(AuditEvent(
        actor_id=current_user.id,
        action="PROFILE_UPDATE",
        entity_type="PROFILE",
        entity_id=profile.id,
        metadata_json={"designation": profile.designation, "department": profile.department}
    ))
    db.commit()
    db.refresh(profile)

    track_code = profile.track.code if profile.track else None
    return ProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        track_id=profile.track_id,
        track_code=track_code,
        designation=profile.designation,
        department=profile.department,
        education_json=profile.education_json,
        experience_json=profile.experience_json,
        career_goal=profile.career_goal,
        target_role_id=profile.target_role_id,
        metadata_json=profile.metadata_json
    )
