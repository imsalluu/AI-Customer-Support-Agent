from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class DocumentCreate(BaseModel):
    title: str
    content: Optional[str] = None
    file_type: str = "TXT"  # PDF, DOCX, TXT, MD, FAQ, POLICY
    source_url: Optional[str] = None


class ChunkResponse(BaseModel):
    id: str
    document_id: str
    chunk_index: int
    content: str
    token_count: int
    source_name: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    similarity_score: Optional[float] = None

    model_config = {"from_attributes": True}


class DocumentResponse(BaseModel):
    id: str
    organization_id: str
    title: str
    file_name: str
    file_type: str
    file_size: int
    status: str
    total_chunks: int
    source_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class KnowledgeSearchQuery(BaseModel):
    query: str
    top_k: int = 5
    min_similarity: float = 0.3


class KnowledgeSearchResult(BaseModel):
    query: str
    results: List[ChunkResponse]
