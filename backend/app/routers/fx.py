from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..db import get_session
from ..models import ExchangeRate
from datetime import date
from ..services.security import require_admin

router = APIRouter(prefix="/fx", tags=["fx"])


@router.get("/rates")
def list_rates(session: Session = Depends(get_session)):
    return session.exec(select(ExchangeRate).order_by(ExchangeRate.currency, ExchangeRate.date.desc())).all()


@router.post("/rates")
def upsert_rate(currency: str, rate_to_base: float, on_date: date | None = None, session: Session = Depends(get_session), admin=Depends(require_admin)):
    d = on_date or date.today()
    # simple insert; in real life unique constraint (currency,date)
    r = ExchangeRate(currency=currency.upper(), date=d, rate_to_base=rate_to_base)
    session.add(r)
    session.commit()
    session.refresh(r)
    return r
