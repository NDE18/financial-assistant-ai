from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # File info
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # 'pdf', 'jpg', 'png'
    
    # Extracted data (via GPT-4 Vision)
    vendor = Column(String, nullable=True)
    invoice_number = Column(String, nullable=True)
    invoice_date = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    total_amount = Column(Float, nullable=True)
    tax_amount = Column(Float, nullable=True)
    currency = Column(String, default="EUR")
    
    # OCR metadata
    extracted_text = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    extraction_status = Column(String, default="pending")  # 'pending', 'success', 'failed'
    
    # Relations
    transaction = relationship("Transaction", back_populates="invoice", uselist=False)
    
    # Status
    is_processed = Column(Boolean, default=False)
    is_paid = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
