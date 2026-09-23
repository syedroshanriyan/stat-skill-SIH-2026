import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User, Profile
from app.schemas.assistant import (
    ChatMessageRequest,
    ChatMessageResponse,
    ConversationResponse,
)
from app.assistant.service import answer_assistant_query

router = APIRouter(prefix="/assistant", tags=["Assistant"])


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    track_code = profile.track.code if profile and profile.track else "GOVERNMENT"

    conv_id = str(uuid.uuid4())
    return ConversationResponse(
        conversation_id=conv_id,
        title=f"{track_code} Competency Assistant Session",
        track=track_code,
        created_at=datetime.now(timezone.utc)
    )


@router.post("/conversations/{conversation_id}/messages", response_model=ChatMessageResponse)
def send_message(
    conversation_id: str,
    payload: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not payload.message.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")

    result = answer_assistant_query(
        db=db,
        user_id=current_user.id,
        conversation_id=conversation_id,
        message=payload.message
    )
    return ChatMessageResponse(**result)
