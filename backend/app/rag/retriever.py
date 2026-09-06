import json
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.knowledge import KnowledgeChunk, KnowledgeDocument
from app.rag.embeddings import cosine_similarity, get_embedding
from app.schemas.conversation import CitationSchema


class RetrievedContext:
    def __init__(self, chunks: List[KnowledgeChunk], citations: List[CitationSchema], grounded_text: str):
        self.chunks = chunks
        self.citations = citations
        self.grounded_text = grounded_text


class KnowledgeRetriever:
    @staticmethod
    async def retrieve(
        db: AsyncSession,
        org_id: str,
        query: str,
        top_k: int = 4,
        min_similarity: float = 0.25,
    ) -> RetrievedContext:
        """Retrieves top matching knowledge chunks with exact citations."""
        query_vec = await get_embedding(query)

        # Query all chunks for tenant
        stmt = (
            select(KnowledgeChunk)
            .options(selectinload(KnowledgeChunk.document))
            .where(KnowledgeChunk.organization_id == org_id)
        )
        res = await db.execute(stmt)
        chunks = res.scalars().all()

        scored_chunks = []
        for chunk in chunks:
            if not chunk.embedding_json:
                continue
            try:
                chunk_vec = json.loads(chunk.embedding_json)
                score = cosine_similarity(query_vec, chunk_vec)
                if score >= min_similarity:
                    scored_chunks.append((score, chunk))
            except Exception:
                continue

        # Sort by similarity descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_scored = scored_chunks[:top_k]

        citations: List[CitationSchema] = []
        context_snippets: List[str] = []
        selected_chunks: List[KnowledgeChunk] = []

        for score, chunk in top_scored:
            selected_chunks.append(chunk)
            doc_title = chunk.document.title if chunk.document else chunk.source_name
            snippet = chunk.content[:300] + ("..." if len(chunk.content) > 300 else "")

            citations.append(
                CitationSchema(
                    document_title=doc_title,
                    source_name=chunk.source_name or doc_title,
                    page_number=chunk.page_number,
                    section_title=chunk.section_title,
                    snippet=snippet,
                    relevance_score=round(score, 3),
                )
            )

            header = f"[{doc_title}"
            if chunk.page_number:
                header += f" | Page {chunk.page_number}"
            if chunk.section_title:
                header += f" | Section: {chunk.section_title}"
            header += "]"

            context_snippets.append(f"{header}\n{chunk.content}")

        grounded_text = "\n\n---\n\n".join(context_snippets) if context_snippets else ""
        return RetrievedContext(chunks=selected_chunks, citations=citations, grounded_text=grounded_text)
