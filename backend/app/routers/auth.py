from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..db import get_session
from ..models import User
from ..services.security import hash_password, verify_password, create_access_token
from ..services.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(email: str, password: str, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    first_user = session.exec(select(User)).first() is None
    role = "admin" if first_user else "user"
    user = User(email=email, hashed_password=hash_password(password), role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(current = Depends(get_current_user)):
    return {"email": current.email, "role": current.role}
