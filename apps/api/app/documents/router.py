import os
import hashlib
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.auth.deps import get_current_user
from app.models.user import User, Membership
from app.models.document import Document, DocumentChunk
from app.models.audit import AuditEvent
from app.schemas.document import DocumentResponse, DocumentChunkResponse, ProcessDocumentResponse
from app.documents.parser import extract_text_and_chunks
from app.rag.embeddings import generate_embedding

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure upload directory exists
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)

    # Read content and compute SHA256
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty")

    sha256_hash = hashlib.sha256(content).hexdigest()

    # Check for duplicate
    existing = db.query(Document).filter(
        Document.user_id == current_user.id,
        Document.sha256 == sha256_hash
    ).first()
    if existing:
        return DocumentResponse(
            id=existing.id,
            user_id=existing.user_id,
            filename=existing.filename,
            mime_type=existing.mime_type,
            sha256=existing.sha256,
            status=existing.status,
            chunk_count=len(existing.chunks),
            created_at=existing.created_at
        )

    # Save to storage
    file_ext = os.path.splitext(file.filename or "file")[1]
    storage_filename = f"{current_user.id}_{sha256_hash[:16]}{file_ext}"
    storage_path = os.path.join(settings.STORAGE_DIR, storage_filename)

    with open(storage_path, "wb") as f:
        f.write(content)

    membership = db.query(Membership).filter(Membership.user_id == current_user.id).first()
    org_id = membership.organization_id if membership else None

    doc = Document(
        user_id=current_user.id,
        organization_id=org_id,
        filename=file.filename or "uploaded_document",
        mime_type=file.content_type or "application/octet-stream",
        storage_key=storage_path,
        sha256=sha256_hash,
        status="uploaded"
    )
    db.add(doc)
    db.add(AuditEvent(
        actor_id=current_user.id,
        organization_id=org_id,
        action="DOCUMENT_UPLOADED",
        entity_type="DOCUMENT",
        entity_id=doc.id,
        metadata_json={"filename": doc.filename, "size_bytes": len(content)}
    ))
    db.commit()
    db.refresh(doc)

    return DocumentResponse(
        id=doc.id,
        user_id=doc.user_id,
        filename=doc.filename,
        mime_type=doc.mime_type,
        sha256=doc.sha256,
        status=doc.status,
        chunk_count=0,
        created_at=doc.created_at
    )


@router.get("", response_model=List[DocumentResponse])
def list_my_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    docs = db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()
    results = []
    for d in docs:
        c_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == d.id).count()
        results.append(DocumentResponse(
            id=d.id,
            user_id=d.user_id,
            filename=d.filename,
            mime_type=d.mime_type,
            sha256=d.sha256,
            status=d.status,
            chunk_count=c_count,
            created_at=d.created_at
        ))
    return results


@router.get("/{document_id}")
def get_document_details(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    membership = db.query(Membership).filter(Membership.user_id == current_user.id).first()
    is_admin = membership and membership.role == "platform_admin"
    in_same_org = membership and doc.organization_id and membership.organization_id == doc.organization_id
    if not (is_admin or in_same_org or doc.user_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Document isolation strictly enforced across tenants and tracks"
        )

    chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).order_by(DocumentChunk.chunk_index).all()
    return {
        "id": doc.id,
        "filename": doc.filename,
        "mime_type": doc.mime_type,
        "status": doc.status,
        "chunk_count": len(chunks),
        "chunks": [
            {
                "id": c.id,
                "chunk_index": c.chunk_index,
                "content": c.content,
                "page_number": c.page_number
            }
            for c in chunks
        ],
        "created_at": doc.created_at
    }


@router.post("/{document_id}/process", response_model=ProcessDocumentResponse)
def process_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    membership = db.query(Membership).filter(Membership.user_id == current_user.id).first()
    is_admin = membership and membership.role == "platform_admin"
    if doc.user_id != current_user.id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Cannot process documents belonging to another user or scope"
        )

    if not os.path.exists(doc.storage_key):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Stored document file missing")

    # Clear existing chunks
    db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).delete()

    # Extract text and chunk
    extracted_chunks = extract_text_and_chunks(doc.storage_key, doc.mime_type)

    # Save chunks with vector embeddings
    for item in extracted_chunks:
        emb = generate_embedding(item["content"])
        chunk = DocumentChunk(
            document_id=doc.id,
            chunk_index=item["chunk_index"],
            content=item["content"],
            page_number=item.get("page_number", 1),
            metadata_json=item.get("metadata_json", {}),
            embedding=emb
        )
        db.add(chunk)

    doc.status = "indexed"
    db.add(AuditEvent(
        actor_id=current_user.id,
        action="DOCUMENT_INDEXED",
        entity_type="DOCUMENT",
        entity_id=doc.id,
        metadata_json={"chunks_indexed": len(extracted_chunks)}
    ))
    db.commit()

    return ProcessDocumentResponse(
        document_id=doc.id,
        status="indexed",
        chunks_created=len(extracted_chunks),
        message=f"Successfully extracted and indexed {len(extracted_chunks)} chunks for grounded RAG and quiz generation."
    )


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    membership = db.query(Membership).filter(Membership.user_id == current_user.id).first()
    is_admin = membership and membership.role == "platform_admin"
    if doc.user_id != current_user.id and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Cannot delete document belonging to another user or scope"
        )

    if os.path.exists(doc.storage_key):
        try:
            os.remove(doc.storage_key)
        except OSError:
            pass

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}
