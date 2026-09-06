from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.tenant import User
from app.schemas.analytics import (
    AnalyticsOverviewResponse,
    DailyVolumeItem,
    IntentDistributionItem,
    SentimentDistributionItem,
    SupportInsightItem,
)
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics & Support Intelligence"])


@router.get("/overview", response_model=AnalyticsOverviewResponse)
async def get_overview(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get high-level customer support KPIs, resolution rate, and CSAT."""
    return await AnalyticsService.get_overview(db, current_user.organization_id)


@router.get("/intents", response_model=List[IntentDistributionItem])
async def get_intents_distribution(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get intent classification breakdown."""
    return await AnalyticsService.get_intents_distribution(db, current_user.organization_id)


@router.get("/sentiment", response_model=List[SentimentDistributionItem])
async def get_sentiment_distribution(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get customer sentiment distribution (Positive, Neutral, Negative, Angry)."""
    return await AnalyticsService.get_sentiment_distribution(db, current_user.organization_id)


@router.get("/volume", response_model=List[DailyVolumeItem])
async def get_daily_volume(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get 7-day conversation volume and AI resolution rate trends."""
    return await AnalyticsService.get_daily_volume(db, current_user.organization_id)


@router.get("/insights", response_model=List[SupportInsightItem])
async def get_ai_weekly_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get proactive weekly AI-generated support intelligence and actionable recommendations."""
    return await AnalyticsService.get_weekly_ai_insights(db, current_user.organization_id)
