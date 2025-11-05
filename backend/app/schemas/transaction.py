from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    description: str
    amount: float
    type: str = Field(..., pattern="^(income|expense)$")
    date: datetime
    tags: Optional[str] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    category_id: Optional[int] = None

class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    date: Optional[datetime] = None
    category_id: Optional[int] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_verified: Optional[bool] = None

class TransactionResponse(TransactionBase):
    id: int
    category_id: Optional[int]
    category_name: Optional[str] = None
    is_recurring: bool
    is_verified: bool
    confidence_score: Optional[float]
    invoice_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True