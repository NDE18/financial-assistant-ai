from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from ..db import get_session
from ..models import Invoice, Document, InvoiceType
from ..services.ocr import extract_text_from_pdf, parse_invoice_text
from datetime import datetime
import os
from ..services.security import require_roles

router = APIRouter(prefix="/invoices", tags=["invoices"])

STORAGE_DIR = os.path.join("storage", "docs")


@router.get("/")
def list_invoices(session: Session = Depends(get_session)):
    from sqlmodel import select
    return session.exec(select(Invoice).order_by(Invoice.created_at.desc())).all()


@router.post("/ocr")
def ocr_invoice(file: UploadFile = File(...), session: Session = Depends(get_session), user=Depends(require_roles(["admin","finance_manager","accountant"]))):
    # Save file
    ts = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    stored_name = f"{ts}_{file.filename}"
    stored_path = os.path.join(STORAGE_DIR, stored_name)
    with open(stored_path, "wb") as f:
        f.write(file.file.read())
    # OCR only PDF in POC
    if not stored_path.lower().endswith(".pdf"):
        return {"error": "Seuls les PDF sont traités dans ce POC"}
    with open(stored_path, 'rb') as fh:
        upload = UploadFile(filename=file.filename, file=fh)
        text = extract_text_from_pdf(upload)
    data = parse_invoice_text(text)
    inv = Invoice(
        type=InvoiceType.payable,
        due_date=datetime.strptime(data.get("due_date"), "%Y-%m-%d").date() if data.get("due_date") else datetime.utcnow().date(),
        amount=float(data.get("amount") or 0.0),
        currency=(data.get("currency") or "EUR").upper(),
        counterparty=data.get("counterparty") or None,
        status="open",
        file_path=stored_path,
    )
    session.add(inv)
    session.commit()
    session.refresh(inv)
    doc = Document(original_filename=file.filename, stored_path=stored_path, invoice_id=inv.id, type="invoice")
    session.add(doc)
    session.commit()
    return inv
