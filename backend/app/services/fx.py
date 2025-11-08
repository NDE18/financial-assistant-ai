from datetime import date
from typing import Optional
from sqlmodel import Session, select
from ..models import ExchangeRate
from ..core.config import settings


def get_rate(session: Session, currency: str, on_date: Optional[date] = None) -> float:
    if currency == settings.BASE_CURRENCY:
        return 1.0
    q = select(ExchangeRate).where(ExchangeRate.currency == currency)
    if on_date:
        q = q.where(ExchangeRate.date <= on_date).order_by(ExchangeRate.date.desc())
    rate = session.exec(q).first()
    return rate.rate_to_base if rate else 1.0  # fallback 1.0 for POC


def convert(session: Session, amount: float, currency: str, on_date: Optional[date] = None) -> float:
    return amount * get_rate(session, currency, on_date)
