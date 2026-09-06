from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AnalyticsOverviewResponse(BaseModel):
    total_conversations: int
    ai_resolved_count: int
    ai_resolution_rate: float
    human_escalated_count: int
    escalation_rate: float
    open_tickets_count: int
    total_tickets_count: int
    avg_response_time_seconds: float
    csat_score: float
    total_feedbacks: int
    positive_sentiment_percent: float
    negative_sentiment_percent: float


class IntentDistributionItem(BaseModel):
    intent: str
    count: int
    percentage: float


class SentimentDistributionItem(BaseModel):
    sentiment: str
    count: int
    percentage: float


class DailyVolumeItem(BaseModel):
    date: str
    total_conversations: int
    ai_resolved: int
    human_escalated: int


class SupportInsightItem(BaseModel):
    id: str
    category: str
    title: str
    description: str
    metric_change: Optional[str] = None
    severity: str = "INFO"  # INFO, WARNING, SUCCESS
    recommended_action: Optional[str] = None
