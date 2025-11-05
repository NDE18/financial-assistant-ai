from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class KPIData(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    savings_rate: float
    largest_expense: Optional[Dict]
    largest_income: Optional[Dict]

class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float
    transaction_count: int

class TrendData(BaseModel):
    date: str
    income: float
    expenses: float
    balance: float

class AnalyticsResponse(BaseModel):
    period_start: datetime
    period_end: datetime
    kpis: KPIData
    category_breakdown: List[CategoryBreakdown]
    trends: List[TrendData]
    insights: List[str]
    alerts: List[str]