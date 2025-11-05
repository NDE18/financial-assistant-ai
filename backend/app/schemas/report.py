from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class ReportCreate(BaseModel):
    title: str
    type: str
    start_date: datetime
    end_date: datetime

class ReportResponse(BaseModel):
    id: int
    title: str
    type: str
    start_date: datetime
    end_date: datetime
    summary: Optional[str]
    insights: Optional[str]
    recommendations: Optional[str]
    file_path: Optional[str]
    status: str
    is_favorite: bool
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

