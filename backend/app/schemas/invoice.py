from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class InvoiceBase(BaseModel):
    filename: str
    file_type: str

class InvoiceCreate(InvoiceBase):
    file_path: str

class InvoiceExtractedData(BaseModel):
    vendor: Optional[str]
    invoice_number: Optional[str]
    invoice_date: Optional[datetime]
    due_date: Optional[datetime]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: str = "EUR"
    extracted_text: Optional[str]
    confidence_score: Optional[float]

class InvoiceResponse(InvoiceBase):
    id: int
    file_path: str
    vendor: Optional[str]
    invoice_number: Optional[str]
    invoice_date: Optional[datetime]
    due_date: Optional[datetime]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: str
    confidence_score: Optional[float]
    extraction_status: str
    is_processed: bool
    is_paid: bool
    created_at: datetime

    class Config:
        from_attributes = True
