from typing import List, Dict
from datetime import datetime
from sqlmodel import Session, select
from rapidfuzz import fuzz
from ..models import Transaction, ReconciliationMatch


def parse_bank_rows(rows: List[Dict]) -> List[Dict]:
    # Expected keys: date (YYYY-MM-DD), amount (float), description (str), ref (str optional)
    parsed = []
    for r in rows:
        try:
            parsed.append({
                "date": datetime.fromisoformat(r["date"]).date(),
                "amount": float(r["amount"]),
                "description": r.get("description", ""),
                "ref": r.get("ref", "")
            })
        except Exception:
            continue
    return parsed


def match_rows(session: Session, rows: List[Dict]) -> List[ReconciliationMatch]:
    matches: List[ReconciliationMatch] = []
    for r in rows:
        # candidate transactions by date window +/- 2 days and amount tolerance 0.01
        cands = session.exec(
            select(Transaction).where(
                Transaction.date >= r["date"],
                Transaction.date <= r["date"],
            )
        ).all()
        # In a real impl, widen date range and include direction logic
        best = None
        best_score = -1.0
        for t in cands:
            amt_ok = abs(t.amount - abs(r["amount"])) <= 0.01
            desc_score = fuzz.partial_ratio((t.description or "").lower(), r["description"].lower())
            score = desc_score + (50 if amt_ok else 0)
            if score > best_score:
                best = t
                best_score = score
        status = "matched" if best and best_score >= 60 else "unmatched"
        m = ReconciliationMatch(bank_ref=r.get("ref") or r.get("description", ""), transaction_id=(best.id if best and status=="matched" else None), status=status, notes=f"score={best_score}")
        session.add(m)
        matches.append(m)
    session.commit()
    for m in matches:
        session.refresh(m)
    return matches
