import json
from typing import List, Optional, Tuple
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.rag.chunker import TextChunker
from app.rag.embeddings import get_embedding
from app.rag.parser import DocumentParser
from app.rag.retriever import KnowledgeRetriever
from app.schemas.knowledge import ChunkResponse, DocumentResponse, KnowledgeSearchResult


class KnowledgeService:
    @staticmethod
    async def list_documents(db: AsyncSession, org_id: str) -> List[KnowledgeDocument]:
        stmt = (
            select(KnowledgeDocument)
            .where(KnowledgeDocument.organization_id == org_id)
            .order_by(KnowledgeDocument.created_at.desc())
        )
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_document_by_id(db: AsyncSession, org_id: str, document_id: str) -> KnowledgeDocument:
        stmt = (
            select(KnowledgeDocument)
            .options(selectinload(KnowledgeDocument.chunks))
            .where(KnowledgeDocument.id == document_id, KnowledgeDocument.organization_id == org_id)
        )
        res = await db.execute(stmt)
        doc = res.scalar_one_or_none()
        if not doc:
            raise NotFoundError("Knowledge Document", document_id)
        return doc

    @staticmethod
    async def ingest_file(
        db: AsyncSession,
        org_id: str,
        file: UploadFile,
        title: Optional[str] = None,
    ) -> KnowledgeDocument:
        file_bytes = await file.read()
        file_name = file.filename or "uploaded_document"
        file_ext = file_name.split(".")[-1].upper() if "." in file_name else "TXT"
        doc_title = title or file_name.rsplit(".", 1)[0].replace("_", " ").title()

        # Parse sections
        sections: List[Tuple[str, int, str]] = []
        if file_ext == "PDF":
            sections = DocumentParser.parse_pdf(file_bytes)
        elif file_ext in ["DOCX", "DOC"]:
            sections = DocumentParser.parse_docx(file_bytes)
        else:
            text_str = file_bytes.decode("utf-8", errors="ignore")
            sections = DocumentParser.parse_text(text_str)

        if not sections:
            sections = [(file_bytes.decode("utf-8", errors="ignore"), 1, "General")]

        # Split into chunks
        chunker = TextChunker(chunk_size=500, chunk_overlap=100)
        parsed_chunks = chunker.split_text(sections)

        # Create Document record
        doc = KnowledgeDocument(
            organization_id=org_id,
            title=doc_title,
            file_name=file_name,
            file_type=file_ext,
            file_size=len(file_bytes),
            status="READY",
            total_chunks=len(parsed_chunks),
        )
        db.add(doc)
        await db.flush()

        # Generate embeddings and save chunks
        for p_chunk in parsed_chunks:
            emb = await get_embedding(p_chunk.content)
            chunk = KnowledgeChunk(
                organization_id=org_id,
                document_id=doc.id,
                chunk_index=p_chunk.chunk_index,
                content=p_chunk.content,
                embedding_json=json.dumps(emb),
                token_count=p_chunk.token_count,
                source_name=doc_title,
                page_number=p_chunk.page_number,
                section_title=p_chunk.section_title,
            )
            db.add(chunk)

        await db.commit()
        await db.refresh(doc)
        return doc

    @staticmethod
    async def ingest_raw_text(
        db: AsyncSession,
        org_id: str,
        title: str,
        content: str,
        file_type: str = "POLICY",
        source_url: Optional[str] = None,
    ) -> KnowledgeDocument:
        sections = DocumentParser.parse_text(content)
        chunker = TextChunker(chunk_size=500, chunk_overlap=100)
        parsed_chunks = chunker.split_text(sections)

        doc = KnowledgeDocument(
            organization_id=org_id,
            title=title,
            file_name=f"{title.lower().replace(' ', '_')}.txt",
            file_type=file_type,
            file_size=len(content.encode("utf-8")),
            status="READY",
            total_chunks=len(parsed_chunks),
            source_url=source_url,
        )
        db.add(doc)
        await db.flush()

        for p_chunk in parsed_chunks:
            emb = await get_embedding(p_chunk.content)
            chunk = KnowledgeChunk(
                organization_id=org_id,
                document_id=doc.id,
                chunk_index=p_chunk.chunk_index,
                content=p_chunk.content,
                embedding_json=json.dumps(emb),
                token_count=p_chunk.token_count,
                source_name=title,
                page_number=p_chunk.page_number,
                section_title=p_chunk.section_title,
            )
            db.add(chunk)

        await db.commit()
        await db.refresh(doc)
        return doc

    @staticmethod
    async def delete_document(db: AsyncSession, org_id: str, document_id: str) -> None:
        doc = await KnowledgeService.get_document_by_id(db, org_id, document_id)
        await db.delete(doc)
        await db.commit()

    @staticmethod
    async def search(
        db: AsyncSession,
        org_id: str,
        query: str,
        top_k: int = 5,
        min_similarity: float = 0.25,
    ) -> KnowledgeSearchResult:
        retrieved = await KnowledgeRetriever.retrieve(
            db,
            org_id,
            query,
            top_k=top_k,
            min_similarity=min_similarity,
        )
        results: List[ChunkResponse] = []
        for citation in retrieved.citations:
            results.append(
                ChunkResponse(
                    id="chunk_res",
                    document_id="doc_res",
                    chunk_index=0,
                    content=citation.snippet,
                    token_count=len(citation.snippet.split()),
                    source_name=citation.source_name,
                    page_number=citation.page_number,
                    section_title=citation.section_title,
                    similarity_score=citation.relevance_score,
                )
            )
        return KnowledgeSearchResult(query=query, results=results)
