from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class ProfileUpdate(BaseModel):
    designation: Optional[str] = None
    department: Optional[str] = None
    education_json: Optional[Dict[str, Any]] = None
    experience_json: Optional[Dict[str, Any]] = None
    career_goal: Optional[str] = None
    target_role_id: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class ProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    track_id: str
    track_code: Optional[str] = None
    designation: Optional[str] = None
    department: Optional[str] = None
    education_json: Optional[Dict[str, Any]] = None
    experience_json: Optional[Dict[str, Any]] = None
    career_goal: Optional[str] = None
    target_role_id: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None


class UserUpdate(BaseModel):
    display_name: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: EmailStr
    display_name: str
    status: str
    track_code: Optional[str] = None
    role: Optional[str] = None
    profile: Optional[ProfileResponse] = None
    created_at: datetime

