from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
from sqlmodel import select
from .fx import convert
from ..core.config import settings
from ..db import engine
from sqlmodel import Session
from ..models import Transaction, Direction, Account, Invoice, Budget, BudgetLine, Alert

scheduler: BackgroundScheduler | None = None


def check_notifications():
    today = date.today()
    with Session(engine) as session:
        # Low cash per account
        accounts = session.exec(select(Account)).all()
        for acc in accounts:
            if acc.current_balance < settings.CASH_MIN_THRESHOLD:
                session.add(Alert(type="cash", severity="warning", message=f"Solde bas sur {acc.name}: {acc.current_balance:.2f} {acc.currency}"))
        # Upcoming invoice due (7 days)
        upcoming = session.exec(select(Invoice).where(Invoice.status == "open", Invoice.due_date <= today + timedelta(days=7))).all()
        for inv in upcoming:
            session.add(Alert(type="invoice_due", severity="info", message=f"Échéance proche: {inv.counterparty} {inv.amount:.2f} {inv.currency} le {inv.due_date}"))
        # Budgets overspend: recompute spent by summing tx in period & category
        budgets = session.exec(select(Budget)).all()
        for b in budgets:
            lines = session.exec(select(BudgetLine).where(BudgetLine.budget_id == b.id)).all()
            for line in lines:
                txs = session.exec(
                    select(Transaction).where(
                        Transaction.category == line.category,
                        Transaction.date >= b.start_date,
                        Transaction.date <= b.end_date,
                    )
                ).all()
                spent = 0.0
                for t in txs:
                    # Convert to base currency for aggregation (optional)
                    acc = session.get(Account, t.account_id) if t.account_id else None
                    cur = acc.currency if acc else settings.BASE_CURRENCY
                    amt = convert(session, t.amount, cur, t.date)
                    if t.direction == Direction.expense:
                        spent += amt
                line.spent_amount = spent
                session.add(line)
                if spent > line.limit_amount:
                    session.add(Alert(type="budget_over", severity="warning", message=f"Budget {b.name}/{line.category} dépassé: {spent:.2f}>{line.limit_amount:.2f}"))
        session.commit()


def start_scheduler():
    global scheduler
    if scheduler:
        return
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_notifications, "interval", minutes=5, id="finance_checks", replace_existing=True)
    scheduler.start()
