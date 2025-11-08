from datetime import date
from collections import defaultdict
from typing import Dict, List
from sqlmodel import Session, select
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from ..models import Transaction, Direction, Account
from .fx import convert


def monthly_net_series(session: Session) -> Dict[str, float]:
    txs = session.exec(select(Transaction)).all()
    acc_cache: dict[int, Account] = {}
    buckets: Dict[str, float] = defaultdict(float)
    for t in txs:
        if t.account_id and t.account_id not in acc_cache:
            acc_cache[t.account_id] = session.get(Account, t.account_id)
        cur = acc_cache[t.account_id].currency if t.account_id else "EUR"
        amt = convert(session, t.amount, cur, t.date)
        key = f"{t.date.year}-{t.date.month:02d}"
        if t.direction == Direction.income:
            buckets[key] += amt
        else:
            buckets[key] -= amt
    return dict(sorted(buckets.items()))


def forecast_next(series: List[float], periods: int = 3) -> List[float]:
    if len(series) < 3:
        # naive: repeat last value
        return [series[-1] if series else 0.0] * periods
    model = SimpleExpSmoothing(series, initialization_method="heuristic").fit(optimized=True)
    return list(model.forecast(periods))
