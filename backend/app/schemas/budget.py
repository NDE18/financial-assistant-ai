from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BudgetBase(BaseModel):
    name: str
    category_id: int
    amount: float
    period: str
    start_date: datetime
    end_date: datetime
    alert_threshold: Optional[float] = 0.8

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    alert_threshold: Optional[float] = None

class BudgetResponse(BudgetBase):
    id: int
    spent: float
    is_exceeded: bool
    category_name: Optional[str] = None
    remaining: float
    percentage_used: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
