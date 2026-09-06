from typing import List, Optional
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_roles
from app.core.constants import Role
from app.core.database import get_db
from app.models.tenant import User
from app.schemas.knowledge import (
    DocumentCreate,
    DocumentResponse,
    KnowledgeSearchQuery,
    KnowledgeSearchResult,
)
from app.services.knowledge_service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Base & RAG"])


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all ingested knowledge documents."""
    return await KnowledgeService.list_documents(db, current_user.organization_id)


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN, Role.SUPPORT_AGENT)),
    db: AsyncSession = Depends(get_db),
):
    """Upload and process a document (PDF, DOCX, TXT, MD, FAQ, Policy)."""
    return await KnowledgeService.ingest_file(db, current_user.organization_id, file, title)


@router.post("/text", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_text_document(
    data: DocumentCreate,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN, Role.SUPPORT_AGENT)),
    db: AsyncSession = Depends(get_db),
):
    """Ingest raw text, policy guidelines, or FAQ content."""
    return await KnowledgeService.ingest_raw_text(
        db,
        current_user.organization_id,
        title=data.title,
        content=data.content or "",
        file_type=data.file_type,
        source_url=data.source_url,
    )


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get single document metadata and status."""
    return await KnowledgeService.get_document_by_id(db, current_user.organization_id, document_id)


@router.delete("/documents/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Delete a document and all its chunks."""
    await KnowledgeService.delete_document(db, current_user.organization_id, document_id)


@router.post("/search", response_model=KnowledgeSearchResult)
async def search_knowledge(
    data: KnowledgeSearchQuery,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Search knowledge base with semantic similarity and view citations."""
    return await KnowledgeService.search(
        db,
        current_user.organization_id,
        data.query,
        top_k=data.top_k,
        min_similarity=data.min_similarity,
    )
