from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.engine import SupportAgentEngine
from app.api.deps import get_current_user, require_roles
from app.core.constants import Role
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.agent_config import AgentConfig
from app.models.customer import Customer
from app.models.tenant import User
from app.schemas.agent_config import AgentConfigResponse, AgentConfigUpdate

router = APIRouter(prefix="/agent-config", tags=["AI Agent Configuration Studio"])


class AgentSandboxTestRequest(BaseModel):
    message: str
    mock_order_number: Optional[str] = None


class AgentSandboxTestResponse(BaseModel):
    response_text: str
    intent: str
    sentiment: str
    confidence: float
    citations: list
    tool_executions: list
    handoff_requested: bool


@router.get("", response_model=AgentConfigResponse)
async def get_agent_config(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the organization's AI Support Agent configuration."""
    stmt = select(AgentConfig).where(AgentConfig.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    cfg = res.scalar_one_or_none()
    if not cfg:
        # Create default
        cfg = AgentConfig(
            organization_id=current_user.organization_id,
            name="SupportIQ Assistant",
            tone="PROFESSIONAL",
            personality_prompt="You are a calm, highly capable, and professional customer support specialist.",
            greeting_message="Hello! How can I assist you with orders, returns, or support today?",
            confidence_threshold=0.75,
            is_active=True,
        )
        db.add(cfg)
        await db.commit()
        await db.refresh(cfg)
    return cfg


@router.put("", response_model=AgentConfigResponse)
async def update_agent_config(
    data: AgentConfigUpdate,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Update AI Agent persona, tone, rules, confidence threshold, and enabled tools."""
    stmt = select(AgentConfig).where(AgentConfig.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    cfg = res.scalar_one_or_none()
    if not cfg:
        raise NotFoundError("AgentConfig", current_user.organization_id)

    if data.name is not None:
        cfg.name = data.name
    if data.avatar_url is not None:
        cfg.avatar_url = data.avatar_url
    if data.tone is not None:
        cfg.tone = data.tone
    if data.language is not None:
        cfg.language = data.language
    if data.personality_prompt is not None:
        cfg.personality_prompt = data.personality_prompt
    if data.greeting_message is not None:
        cfg.greeting_message = data.greeting_message
    if data.business_hours_json is not None:
        cfg.business_hours_json = data.business_hours_json
    if data.escalation_rules_json is not None:
        cfg.escalation_rules_json = data.escalation_rules_json
    if data.confidence_threshold is not None:
        cfg.confidence_threshold = data.confidence_threshold
    if data.enabled_tools_json is not None:
        cfg.enabled_tools_json = data.enabled_tools_json
    if data.is_active is not None:
        cfg.is_active = data.is_active

    await db.commit()
    await db.refresh(cfg)
    return cfg


@router.post("/test", response_model=AgentSandboxTestResponse)
async def test_agent_sandbox(
    data: AgentSandboxTestRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Live test agent responses in the AI Agent Studio sandbox."""
    # Find or create a temporary mock customer for testing
    mock_cust = Customer(
        organization_id=current_user.organization_id,
        name=current_user.full_name,
        email=current_user.email,
        total_orders=1,
        lifetime_value=120.0,
    )

    result = await SupportAgentEngine.process_message(
        db=db,
        org_id=current_user.organization_id,
        customer=mock_cust,
        conversation_id="sandbox_conv",
        message_text=data.message,
        conversation_history=[],
    )

    return AgentSandboxTestResponse(
        response_text=result.response_text,
        intent=result.intent,
        sentiment=result.sentiment,
        confidence=result.confidence,
        citations=[c.model_dump() for c in result.citations],
        tool_executions=[t.model_dump() for t in result.tool_executions],
        handoff_requested=result.handoff_requested,
    )
