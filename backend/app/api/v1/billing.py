from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_roles
from app.core.constants import PlanType, Role
from app.core.database import get_db
from app.models.billing import Subscription
from app.models.knowledge import KnowledgeDocument
from app.models.tenant import Organization, User
from app.schemas.billing import PlanChangeRequest, SubscriptionResponse
from app.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate

router = APIRouter(prefix="/billing", tags=["Billing & Subscription Management"])


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get the organization's active subscription tier and resource usage."""
    stmt = select(Subscription).where(Subscription.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    sub = res.scalar_one_or_none()

    if not sub:
        sub = Subscription(
            organization_id=current_user.organization_id,
            plan=PlanType.STARTER.value,
            is_active=True,
            max_monthly_messages=5000,
            current_month_messages=210,
            max_knowledge_docs=20,
            max_agents=5,
        )
        db.add(sub)
        await db.commit()
        await db.refresh(sub)

    # Count docs
    doc_stmt = select(func.count(KnowledgeDocument.id)).where(KnowledgeDocument.organization_id == current_user.organization_id)
    doc_res = await db.execute(doc_stmt)
    doc_count = doc_res.scalar_one() or 0

    # Count agents
    agent_stmt = select(func.count(User.id)).where(User.organization_id == current_user.organization_id)
    agent_res = await db.execute(agent_stmt)
    agent_count = agent_res.scalar_one() or 1

    return SubscriptionResponse(
        id=sub.id,
        organization_id=sub.organization_id,
        plan=sub.plan,
        is_active=sub.is_active,
        max_monthly_messages=sub.max_monthly_messages,
        current_month_messages=sub.current_month_messages or 210,
        max_knowledge_docs=sub.max_knowledge_docs,
        current_docs_count=doc_count,
        max_agents=sub.max_agents,
        current_agents_count=agent_count,
        current_period_end=sub.current_period_end,
    )


@router.post("/change-plan", response_model=SubscriptionResponse)
async def change_subscription_plan(
    data: PlanChangeRequest,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Upgrade or switch organization subscription tier."""
    stmt = select(Subscription).where(Subscription.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    sub = res.scalar_one_or_none()

    plan_limits = {
        PlanType.FREE.value: {"messages": 500, "docs": 3, "agents": 1},
        PlanType.STARTER.value: {"messages": 5000, "docs": 20, "agents": 5},
        PlanType.BUSINESS.value: {"messages": 25000, "docs": 100, "agents": 25},
        PlanType.ENTERPRISE.value: {"messages": 200000, "docs": 1000, "agents": 100},
    }

    limits = plan_limits.get(data.plan, plan_limits[PlanType.STARTER.value])

    if sub:
        sub.plan = data.plan
        sub.max_monthly_messages = limits["messages"]
        sub.max_knowledge_docs = limits["docs"]
        sub.max_agents = limits["agents"]
    else:
        sub = Subscription(
            organization_id=current_user.organization_id,
            plan=data.plan,
            is_active=True,
            max_monthly_messages=limits["messages"],
            max_knowledge_docs=limits["docs"],
            max_agents=limits["agents"],
        )
        db.add(sub)

    # Also update Organization table
    org_stmt = select(Organization).where(Organization.id == current_user.organization_id)
    org_res = await db.execute(org_stmt)
    org = org_res.scalar_one_or_none()
    if org:
        org.plan = data.plan

    await db.commit()
    await db.refresh(sub)
    return await get_subscription(current_user, db)
