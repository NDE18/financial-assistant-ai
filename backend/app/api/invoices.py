from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import os
import base64
from datetime import datetime

from app.database import get_db
from app.models.invoice import Invoice
from app.schemas.invoice import InvoiceResponse, InvoiceExtractedData
from app.agents.orchestrator import OrchestratorAgent
from app.config import get_settings
import json

router = APIRouter()
settings = get_settings()

@router.post("/upload", response_model=InvoiceResponse, status_code=201)
async def upload_invoice(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Upload and process invoice with OCR"""
    
    # Validate file type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save file
    os.makedirs(settings.INVOICE_PATH, exist_ok=True)
    file_path = os.path.join(
        settings.INVOICE_PATH,
        f"{datetime.now().timestamp()}_{file.filename}"
    )
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Create invoice record
    file_ext = file.filename.split('.')[-1].lower()
    db_invoice = Invoice(
        filename=file.filename,
        file_path=file_path,
        file_type=file_ext,
        extraction_status="pending"
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    
    # Background OCR processing
    background_tasks.add_task(
        process_invoice_ocr,
        db_invoice.id,
        file_path,
        content
    )
    
    return db_invoice

async def process_invoice_ocr(invoice_id: int, file_path: str, file_content: bytes):
    """Background task for invoice OCR"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Convert to base64 for GPT-4 Vision
        image_base64 = base64.b64encode(file_content).decode('utf-8')
        
        orchestrator = OrchestratorAgent()
        crew = orchestrator.process_invoice_workflow(file_path, image_base64)
        result = crew.kickoff()
        
        # Parse OCR results
        ocr_data = json.loads(result)
        
        # Update invoice
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            invoice.vendor = ocr_data.get('vendor')
            invoice.invoice_number = ocr_data.get('invoice_number')
            invoice.invoice_date = ocr_data.get('invoice_date')
            invoice.due_date = ocr_data.get('due_date')
            invoice.total_amount = ocr_data.get('total_amount')
            invoice.tax_amount = ocr_data.get('tax_amount')
            invoice.currency = ocr_data.get('currency', 'EUR')
            invoice.extracted_text = ocr_data.get('extracted_text')
            invoice.confidence_score = ocr_data.get('confidence_score')
            invoice.extraction_status = "success"
            invoice.is_processed = True
            
            db.commit()
            
            # Create associated transaction
            from app.models.transaction import Transaction
            if invoice.total_amount:
                transaction = Transaction(
                    description=f"Invoice from {invoice.vendor or 'Unknown'}",
                    amount=invoice.total_amount,
                    type="expense",
                    date=invoice.invoice_date or datetime.utcnow(),
                    invoice_id=invoice.id,
                    notes=f"Invoice #{invoice.invoice_number}"
                )
                db.add(transaction)
                db.commit()
    except Exception as e:
        # Mark as failed
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if invoice:
            invoice.extraction_status = "failed"
            db.commit()
    finally:
        db.close()

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all invoices"""
    
    query = db.query(Invoice)
    if status:
        query = query.filter(Invoice.extraction_status == status)
    
    invoices = query.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()
    return invoices

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Get invoice by ID"""
    
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice

@router.delete("/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """Delete invoice"""
    
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    # Delete file
    if os.path.exists(invoice.file_path):
        os.remove(invoice.file_path)
    
    db.delete(invoice)
    db.commit()
    
    return None
