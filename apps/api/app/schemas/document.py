from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DocumentChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    chunk_index: int
    content: str
    page_number: Optional[int] = None
    metadata_json: Optional[Dict[str, Any]] = None


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    filename: str
    mime_type: str
    sha256: str
    status: str  # uploaded, processing, indexed, failed
    chunk_count: Optional[int] = 0
    created_at: datetime



class ProcessDocumentResponse(BaseModel):
    document_id: str
    status: str
    chunks_created: int
    message: str
