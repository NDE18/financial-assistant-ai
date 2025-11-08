from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..db import get_session
from ..models import User
from ..services.security import require_admin, hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def list_users(session: Session = Depends(get_session), admin=Depends(require_admin)):
    return session.exec(select(User).order_by(User.id)).all()


@router.post("/")
def create_user(email: str, password: str, role: str = "user", session: Session = Depends(get_session), admin=Depends(require_admin)):
    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(email=email, hashed_password=hash_password(password), role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "email": user.email, "role": user.role, "is_active": user.is_active}


@router.patch("/{user_id}/activate")
def set_active(user_id: int, is_active: bool, session: Session = Depends(get_session), admin=Depends(require_admin)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = is_active
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "is_active": user.is_active}


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session), admin=Depends(require_admin)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": "deleted"}