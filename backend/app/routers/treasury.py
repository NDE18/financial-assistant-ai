from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import get_session
from ..services.treasury import monthly_net_series, forecast_next

router = APIRouter(prefix="/treasury", tags=["treasury"])


@router.get("/forecast")
def forecast(session: Session = Depends(get_session)):
    series = monthly_net_series(session)
    xs = list(series.keys())
    ys = list(series.values())
    preds = forecast_next(ys, periods=3)
    return {"months": xs, "values": ys, "forecast": preds}
