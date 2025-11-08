from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import Transaction, Invoice, Budget, Document
from typing import Dict

router = APIRouter(prefix="/search", tags=["search"])


def _like(field, q: str):
    # portable LIKE with wildcards around q
    return field.ilike(f"%{q}%") if hasattr(field, 'ilike') else field.contains(q)


@router.get("/")
def search(q: str, session: Session = Depends(get_session)) -> Dict:
    q = q.strip()
    if not q:
        return {"transactions": [], "invoices": [], "budgets": [], "documents": []}

    txs = session.exec(
        select(Transaction)
        .where((Transaction.description.ilike(f"%{q}%")) | (Transaction.category.ilike(f"%{q}%")))
        .order_by(Transaction.date.desc())
        .limit(10)
    ).all()

    invs = session.exec(
        select(Invoice)
        .where((Invoice.counterparty.ilike(f"%{q}%")))
        .order_by(Invoice.created_at.desc())
        .limit(10)
    ).all()

    buds = session.exec(
        select(Budget)
        .where(Budget.name.ilike(f"%{q}%"))
        .order_by(Budget.start_date.desc())
        .limit(10)
    ).all()

    docs = session.exec(
        select(Document)
        .where(Document.original_filename.ilike(f"%{q}%"))
        .order_by(Document.uploaded_at.desc())
        .limit(10)
    ).all()

    return {
        "transactions": txs,
        "invoices": invs,
        "budgets": buds,
        "documents": docs,
    }
