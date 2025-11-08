from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from ..db import get_session
from ..models import Alert
from sqlmodel import select

router = APIRouter(prefix="/notifications", tags=["notifications"])


from ..services.security import get_current_user

@router.get("/")
def list_alerts(session: Session = Depends(get_session), user=Depends(get_current_user)):
    return session.exec(select(Alert).order_by(Alert.created_at.desc())).all()

@router.patch("/{alert_id}/resolve")
def resolve_alert(alert_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    alert = session.get(Alert, alert_id)
    if not alert:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.resolved = True
    session.add(alert)
    session.commit()
    session.refresh(alert)
    return alert
