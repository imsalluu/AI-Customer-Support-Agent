import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.intent_sentiment import IntentSentimentClassifier
from app.agents.llm_client import LLMClient
from app.core.constants import ConversationStatus, IntentType, SentimentType, TicketCategory, TicketPriority
from app.models.agent_config import AgentConfig
from app.models.conversation import Message
from app.models.customer import Customer
from app.rag.retriever import KnowledgeRetriever
from app.schemas.conversation import CitationSchema, ToolExecutionSchema
from app.tools.implementations import (
    tool_check_inventory,
    tool_check_shipping,
    tool_create_support_ticket,
    tool_get_order_status,
    tool_get_product,
    tool_request_human_agent,
    tool_search_customer,
    tool_search_products,
)


class AgentExecutionResult:
    def __init__(
        self,
        response_text: str,
        intent: str,
        sentiment: str,
        confidence: float,
        citations: List[CitationSchema],
        tool_executions: List[ToolExecutionSchema],
        handoff_requested: bool = False,
        summary_update: Optional[str] = None,
    ):
        self.response_text = response_text
        self.intent = intent
        self.sentiment = sentiment
        self.confidence = confidence
        self.citations = citations
        self.tool_executions = tool_executions
        self.handoff_requested = handoff_requested
        self.summary_update = summary_update


class SupportAgentEngine:
    @staticmethod
    async def process_message(
        db: AsyncSession,
        org_id: str,
        customer: Customer,
        conversation_id: str,
        message_text: str,
        conversation_history: List[Dict[str, str]],
    ) -> AgentExecutionResult:
        # Load agent config
        cfg_stmt = select(AgentConfig).where(AgentConfig.organization_id == org_id)
        cfg_res = await db.execute(cfg_stmt)
        agent_config = cfg_res.scalar_one_or_none()

        confidence_threshold = agent_config.confidence_threshold if agent_config else 0.75
        system_prompt = agent_config.personality_prompt if agent_config else "You are SupportIQ customer support."

        # 1. Intent & Sentiment Classification & Entity Extraction
        intent = IntentSentimentClassifier.classify_intent(message_text)
        sentiment = IntentSentimentClassifier.analyze_sentiment(message_text)
        entities = IntentSentimentClassifier.extract_entities(message_text)

        tool_executions: List[ToolExecutionSchema] = []
        citations: List[CitationSchema] = []
        handoff_requested = False
        confidence = 0.95
        tool_results_raw: List[Dict[str, Any]] = []

        # 2. Check for Immediate Human Handoff triggers
        if intent == IntentType.HUMAN_REQUEST.value or sentiment == SentimentType.ANGRY.value:
            handoff_requested = True
            urgency = "URGENT" if sentiment == SentimentType.ANGRY.value else "NORMAL"
            reason = f"Customer sentiment: {sentiment}, Intent: {intent}"
            
            tool_out = await tool_request_human_agent(
                db, org_id, reason=reason, urgency=urgency, conversation_id=conversation_id
            )
            tool_executions.append(
                ToolExecutionSchema(
                    tool_name="request_human_agent",
                    arguments={"reason": reason, "urgency": urgency},
                    output=tool_out,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                )
            )
            tool_results_raw.append({"tool_name": "request_human_agent", "output": tool_out})

            # Auto create ticket for angry complaint
            if sentiment == SentimentType.ANGRY.value:
                ticket_out = await tool_create_support_ticket(
                    db,
                    org_id,
                    customer_id=customer.id,
                    subject=f"Urgent Complaint: {message_text[:60]}...",
                    description=f"Customer expressed high frustration. Message: {message_text}",
                    priority=TicketPriority.URGENT.value,
                    category=TicketCategory.COMPLAINT.value,
                    conversation_id=conversation_id,
                )
                tool_executions.append(
                    ToolExecutionSchema(
                        tool_name="create_support_ticket",
                        arguments={"priority": "URGENT", "category": "COMPLAINT"},
                        output=ticket_out,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )
                tool_results_raw.append({"tool_name": "create_support_ticket", "output": ticket_out})

            response_text = (
                "I understand your concern and I apologize for any inconvenience. "
                "I have prioritized your request and am immediately transferring you to a senior human support specialist. "
                "A support ticket has been created and our team is stepping in right now."
            )

            return AgentExecutionResult(
                response_text=response_text,
                intent=intent,
                sentiment=sentiment,
                confidence=1.0,
                citations=[],
                tool_executions=tool_executions,
                handoff_requested=True,
                summary_update=f"Customer escalated with sentiment {sentiment}. Topic: {intent}.",
            )

        # 3. Tool Calling Routing
        if intent == IntentType.ORDER_STATUS.value:
            order_num = entities.get("order_number")
            if order_num:
                res = await tool_get_order_status(db, org_id, order_num)
                tool_executions.append(
                    ToolExecutionSchema(
                        tool_name="get_order_status",
                        arguments={"order_id_or_number": order_num},
                        output=res,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )
                tool_results_raw.append({"tool_name": "get_order_status", "output": res})
                if not res.get("found"):
                    confidence = 0.70
            else:
                # Ask customer for order number
                pass

        elif intent == IntentType.SHIPPING.value:
            order_num = entities.get("order_number")
            if order_num:
                res = await tool_check_shipping(db, org_id, order_num)
                tool_executions.append(
                    ToolExecutionSchema(
                        tool_name="check_shipping",
                        arguments={"tracking_number_or_order": order_num},
                        output=res,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )
                tool_results_raw.append({"tool_name": "check_shipping", "output": res})

        elif intent == IntentType.PRODUCT_INFO.value:
            sku = entities.get("sku")
            if sku:
                res = await tool_get_product(db, org_id, sku)
                tool_executions.append(
                    ToolExecutionSchema(
                        tool_name="get_product",
                        arguments={"product_id_or_sku": sku},
                        output=res,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )
                tool_results_raw.append({"tool_name": "get_product", "output": res})
            else:
                # Search products by query terms
                query_term = message_text.replace("price", "").replace("product", "").strip()
                res = await tool_search_products(db, org_id, query=query_term)
                tool_executions.append(
                    ToolExecutionSchema(
                        tool_name="search_products",
                        arguments={"query": query_term},
                        output=res,
                        timestamp=datetime.now(timezone.utc).isoformat(),
                    )
                )
                tool_results_raw.append({"tool_name": "search_products", "output": res})

        # 4. RAG Knowledge Base Retrieval
        retrieved = await KnowledgeRetriever.retrieve(
            db, org_id, query=message_text, top_k=3, min_similarity=0.20
        )
        citations = retrieved.citations

        # 5. Generate Grounded Response
        grounded_text = retrieved.grounded_text
        response_text = await LLMClient.generate_response(
            system_prompt=system_prompt,
            user_message=message_text,
            conversation_history=conversation_history,
            grounded_context=grounded_text,
            tool_results=tool_results_raw,
        )

        # 6. Confidence & Safety Evaluation
        # If no tools called, no RAG citations found, and message was complex/unrecognized
        if not tool_executions and not citations and len(message_text.split()) > 4:
            confidence = 0.60

        if confidence < confidence_threshold:
            # Fallback to human escalation rather than guessing
            handoff_requested = True
            response_text = (
                "I want to make sure I give you the exact right information regarding your inquiry. "
                "Let me connect you with one of our support specialists who can look into this for you right away."
            )

        summary_update = f"Discussed {intent.lower().replace('_', ' ')} with sentiment {sentiment.lower()}."

        return AgentExecutionResult(
            response_text=response_text,
            intent=intent,
            sentiment=sentiment,
            confidence=confidence,
            citations=citations,
            tool_executions=tool_executions,
            handoff_requested=handoff_requested,
            summary_update=summary_update,
        )
