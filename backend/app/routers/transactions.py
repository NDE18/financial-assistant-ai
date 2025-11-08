from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List, Optional
from datetime import date
from sqlmodel import select
from ..db import get_session
from ..models import Transaction, Direction
from sqlmodel import Session
import csv
import io
from ..services.security import get_current_user

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/", response_model=List[Transaction])
def list_transactions(
    session: Session = Depends(get_session),
    account_id: Optional[int] = None,
):
    query = select(Transaction)
    if account_id:
        query = query.where(Transaction.account_id == account_id)
    results = session.exec(query.order_by(Transaction.date.desc(), Transaction.id.desc())).all()
    return results


from ..services.security import require_roles

@router.post("/", response_model=Transaction)

def create_transaction(
    tx: Transaction,
    session: Session = Depends(get_session),
    user=Depends(require_roles(["admin","finance_manager","accountant"])),
):
    if tx.id is not None:
        tx.id = None
    # Normalize date if received as ISO string
    if isinstance(tx.date, str):
        tx.date = date.fromisoformat(tx.date)
    session.add(tx)
    session.commit()
    session.refresh(tx)
    return tx


@router.post("/import_csv")
def import_csv(
    file: UploadFile = File(...),
    account_id: Optional[int] = None,
    session: Session = Depends(get_session),
    user=Depends(require_roles(["admin","finance_manager","accountant"])),
):
    if not file.filename.endswith((".csv", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    created = 0
    for row in reader:
        try:
            amount = float(row.get("amount") or row.get("Amount"))
            direction = Direction.expense if amount < 0 else Direction.income
            tx = Transaction(
                account_id=account_id,
                date=date.fromisoformat(row.get("date") or row.get("Date")),
                amount=abs(amount),
                direction=direction,
                category=row.get("category") or None,
                description=row.get("description") or row.get("Description"),
            )
            session.add(tx)
            created += 1
        except Exception:  # noqa: BLE001
            continue
    session.commit()
    return {"imported": created}

@router.post("/categorize")

def categorize_uncategorized(session: Session = Depends(get_session), user=Depends(require_roles(["admin","finance_manager","accountant"]))):
    from ..agents.crew import categorize_with_crew

    txs = session.exec(select(Transaction).where(Transaction.category.is_(None))).all()
    if not txs:
        return {"updated": 0}

    rows = [
        {
            "id": t.id,
            "date": str(t.date),
            "amount": t.amount,
            "direction": t.direction.value,
            "description": t.description or "",
        }
        for t in txs
    ]
    cats = categorize_with_crew(rows)
    for tx, cat in zip(txs, cats):
        tx.category = cat
        session.add(tx)
    session.commit()
    return {"updated": len(cats)}
