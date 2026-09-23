from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime


class MessageCitation(BaseModel):
    document_title: str
    page_number: Optional[int] = None
    chunk_text: str
    relevance_score: float


class ToolExecution(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    result: Any


class ChatMessageRequest(BaseModel):
    message: str
    context_filters: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    message_id: str
    conversation_id: str
    role: str = "assistant"
    content: str
    citations: List[MessageCitation] = []
    tools_executed: List[ToolExecution] = []
    created_at: datetime


class ConversationResponse(BaseModel):
    conversation_id: str
    title: str
    track: str
    created_at: datetime
