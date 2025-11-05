from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from app.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'monthly', 'quarterly', 'custom'
    
    # Report period
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    
    # Content
    summary = Column(Text, nullable=True)
    insights = Column(Text, nullable=True)  # JSON string
    recommendations = Column(Text, nullable=True)  # JSON string
    
    # File
    file_path = Column(String, nullable=True)
    file_format = Column(String, default="pdf")
    
    # Status
    status = Column(String, default="generating")  # 'generating', 'completed', 'failed'
    is_favorite = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)