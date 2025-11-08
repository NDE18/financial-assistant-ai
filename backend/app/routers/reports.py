from fastapi import APIRouter, Depends
from datetime import date
from typing import Dict
from sqlmodel import select, func
from ..db import get_session
from ..models import Transaction, Direction, Account, Budget, BudgetLine
from sqlmodel import Session, select
from ..services.fx import convert
from ..services.security import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/monthly")
def monthly_report(year: int, month: int, session: Session = Depends(get_session), user=Depends(get_current_user)) -> Dict:
    start = date(year, month, 1)
    end = date(year + (1 if month == 12 else 0), (1 if month == 12 else month + 1), 1)

    # Fetch transactions and convert amounts to base currency
    txs = session.exec(
        select(Transaction).where(
            Transaction.date >= start,
            Transaction.date < end,
        )
    ).all()
    # build account cache
    acc_cache: dict[int, Account] = {}
    income = 0.0
    expense = 0.0
    for t in txs:
        if t.account_id and t.account_id not in acc_cache:
            acc_cache[t.account_id] = session.get(Account, t.account_id)
        currency = acc_cache[t.account_id].currency if t.account_id else "EUR"
        amt = convert(session, t.amount, currency, t.date)
        if t.direction == Direction.income:
            income += amt
        else:
            expense += amt
    net = income - expense

    # Generate a narrative via CrewAI orchestrated agent
    from ..agents.crew import summarize_with_crew

    narrative = summarize_with_crew({
        "income": float(income or 0),
        "expense": float(expense or 0),
        "net": float(net),
        "year": year,
        "month": month,
    })

    return {
        "period": {"year": year, "month": month},
        "income": income or 0,
        "expense": expense or 0,
        "net": net,
        "narrative": narrative,
    }


@router.get("/quarterly")
def quarterly_report(year: int, quarter: int, session: Session = Depends(get_session)) -> Dict:
    from datetime import date as dt_date
    if quarter not in (1, 2, 3, 4):
        quarter = 1
    start_month = {1: 1, 2: 4, 3: 7, 4: 10}[quarter]
    start = dt_date(year, start_month, 1)
    # compute end as first day of next quarter
    if quarter == 4:
        end = dt_date(year + 1, 1, 1)
    else:
        end = dt_date(year, start_month + 3, 1)

    txs = session.exec(
        select(Transaction).where(
            Transaction.date >= start,
            Transaction.date < end,
        )
    ).all()
    acc_cache: dict[int, Account] = {}
    income = 0.0
    expense = 0.0
    for t in txs:
        if t.account_id and t.account_id not in acc_cache:
            acc_cache[t.account_id] = session.get(Account, t.account_id)
        currency = acc_cache[t.account_id].currency if t.account_id else "EUR"
        amt = convert(session, t.amount, currency, t.date)
        if t.direction == Direction.income:
            income += amt
        else:
            expense += amt
    net = income - expense
    return {
        "year": year,
        "quarter": quarter,
        "income": income,
        "expense": expense,
        "net": net,
    }

@router.get("/annual")
def annual_report(year: int, session: Session = Depends(get_session)) -> Dict:
    from datetime import date as dt_date
    start = dt_date(year, 1, 1)
    end = dt_date(year + 1, 1, 1)

    # Aggregate transactions in base currency
    txs = session.exec(
        select(Transaction).where(
            Transaction.date >= start,
            Transaction.date < end,
        )
    ).all()
    acc_cache: dict[int, Account] = {}
    income = 0.0
    expense = 0.0
    for t in txs:
        if t.account_id and t.account_id not in acc_cache:
            acc_cache[t.account_id] = session.get(Account, t.account_id)
        currency = acc_cache[t.account_id].currency if t.account_id else "EUR"
        amt = convert(session, t.amount, currency, t.date)
        if t.direction == Direction.income:
            income += amt
        else:
            expense += amt
    net = income - expense

    # Annual budget: sum budgets overlapping the year (simple sum for POC)
    budgets = session.exec(
        select(Budget).where(
            Budget.start_date < end,
            Budget.end_date >= start,
        )
    ).all()
    budget_total = sum(b.total_amount for b in budgets)

    return {
        "year": year,
        "income": income,
        "expense": expense,
        "net": net,
        "budget_total": budget_total,
        "budget_consumed": expense,  # treat expenses as consumption
        "budget_remaining": max(budget_total - expense, 0.0),
    }
