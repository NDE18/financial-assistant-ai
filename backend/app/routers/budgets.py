from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import select, Session
from datetime import date as dt_date
from ..db import get_session
from ..models import Budget, BudgetLine
from ..services.security import require_roles

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/", response_model=List[Budget])
def list_budgets(session: Session = Depends(get_session)):
    return session.exec(select(Budget)).all()


@router.post("/", response_model=Budget)
def create_budget(
    b: Budget,
    session: Session = Depends(get_session),
    user=Depends(require_roles(["admin", "finance_manager"])),
) -> Budget:
    if b.id is not None:
        b.id = None
    # Normalize dates in case they arrived as strings
    if isinstance(b.start_date, str):
        b.start_date = dt_date.fromisoformat(b.start_date)
    if isinstance(b.end_date, str):
        b.end_date = dt_date.fromisoformat(b.end_date)
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


@router.get("/{budget_id}/lines", response_model=List[BudgetLine])
def list_lines(budget_id: int, session: Session = Depends(get_session)):
    return session.exec(select(BudgetLine).where(BudgetLine.budget_id == budget_id)).all()


@router.post("/{budget_id}/lines", response_model=BudgetLine)
def add_line(
    budget_id: int,
    line: BudgetLine,
    session: Session = Depends(get_session),
    user=Depends(require_roles(["admin", "finance_manager"])),
) -> BudgetLine:
    line.id = None
    line.budget_id = budget_id
    session.add(line)
    session.commit()
    session.refresh(line)
    return line
