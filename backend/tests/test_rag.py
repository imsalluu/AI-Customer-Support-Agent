import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tenant import Organization
from app.rag.chunker import TextChunker
from app.rag.parser import DocumentParser
from app.rag.retriever import KnowledgeRetriever
from app.services.knowledge_service import KnowledgeService


@pytest.mark.asyncio
async def test_rag_pipeline_and_citation_retrieval(db_session: AsyncSession, test_org: Organization):
    policy_text = """# Return Policy
Customers can return any product within 30 days of purchase for a 100% full refund.
Returned products must be in original packaging with all included accessories.

# International Shipping Policy
We ship to over 50 countries worldwide via DHL Express. Delivery takes 5 to 7 business days.
Import duties and customs taxes are paid at checkout."""

    # Ingest document
    doc = await KnowledgeService.ingest_raw_text(
        db_session,
        test_org.id,
        title="Apex Store Policies",
        content=policy_text,
    )
    assert doc.id is not None
    assert doc.total_chunks > 0

    # Search for return policy
    retrieved = await KnowledgeRetriever.retrieve(
        db_session,
        test_org.id,
        query="What is your return window for a refund?",
        top_k=2,
    )
    assert len(retrieved.citations) > 0
    assert "30 days" in retrieved.citations[0].snippet or "refund" in retrieved.citations[0].snippet
    assert retrieved.citations[0].document_title == "Apex Store Policies"
