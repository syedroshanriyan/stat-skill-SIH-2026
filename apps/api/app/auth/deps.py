from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User, Membership, Profile, Track

security_scheme = HTTPBearer(auto_error=False)


class AuthContext:
    def __init__(
        self,
        user: User,
        roles: List[str],
        organization_ids: List[str],
        track_code: str
    ):
        self.user = user
        self.roles = roles
        self.organization_ids = organization_ids
        self.track_code = track_code
        self.is_platform_admin = "platform_admin" in roles

    def has_role(self, role: str) -> bool:
        return self.is_platform_admin or role in self.roles

    def has_any_role(self, allowed_roles: List[str]) -> bool:
        if self.is_platform_admin:
            return True
        return any(r in allowed_roles for r in self.roles)

    def can_access_org(self, organization_id: Optional[str]) -> bool:
        if self.is_platform_admin:
            return True
        if not organization_id:
            return True
        return organization_id in self.organization_ids

    def can_access_track(self, track_code: str) -> bool:
        if self.is_platform_admin:
            return True
        return self.track_code == track_code


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user_id = payload["sub"]
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return user


def get_auth_context(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AuthContext:
    memberships = db.query(Membership).filter(Membership.user_id == current_user.id).all()
    roles = [m.role for m in memberships]
    org_ids = [m.organization_id for m in memberships if m.organization_id]

    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    track_code = "GOVERNMENT"
    if profile and profile.track_id:
        track = db.query(Track).filter(Track.id == profile.track_id).first()
        if track:
            track_code = track.code

    return AuthContext(
        user=current_user,
        roles=roles,
        organization_ids=org_ids,
        track_code=track_code
    )


def require_roles(allowed_roles: List[str]):
    def role_checker(
        context: AuthContext = Depends(get_auth_context)
    ) -> User:
        if not context.has_any_role(allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Action requires one of authorized roles: {', '.join(allowed_roles)}"
            )
        return context.user

    return role_checker


def require_platform_admin(
    context: AuthContext = Depends(get_auth_context)
) -> User:
    if not context.is_platform_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to Platform Administrator only"
        )
    return context.user
