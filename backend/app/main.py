from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .db import init_db
from .core.config import settings
from .routers import transactions, budgets, reports, analysis, reconciliation, documents, notifications, treasury, auth, invoices, fx, users, search

app = FastAPI(title="Financial Assistant AI (POC)")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(transactions)
app.include_router(budgets)
app.include_router(reports)
app.include_router(analysis)
app.include_router(reconciliation)
app.include_router(documents)
app.include_router(notifications)
app.include_router(treasury)
app.include_router(auth)
app.include_router(invoices)
app.include_router(fx)
app.include_router(users)
app.include_router(search)


@app.on_event("startup")
def on_startup():
    # Ensure storage dirs
    os.makedirs(os.path.join("storage", "docs"), exist_ok=True)
    init_db()
    # Seed demo users if missing
    from .services.security import hash_password
    from .models import User
    from sqlmodel import Session
    from .db import engine
    with Session(engine) as s:
        from sqlmodel import select
        from .services.security import verify_password
        def ensure(email, pwd, role):
            u = s.exec(select(User).where(User.email==email)).first()
            if not u:
                u = User(email=email, hashed_password=hash_password(pwd), role=role, is_active=True)
                s.add(u)
                s.commit()
            else:
                # Ensure role is correct
                if u.role != role:
                    u.role = role
                # Ensure password hash is valid for the expected password (handles bcrypt->pbkdf2 migrations)
                if not verify_password(pwd, u.hashed_password):
                    u.hashed_password = hash_password(pwd)
                s.add(u)
                s.commit()
        ensure("admin@example.com", "Passw0rd!", "admin")
        ensure("finance@example.com", "Passw0rd!", "finance_manager")
        ensure("accountant@example.com", "Passw0rd!", "accountant")
        ensure("user@example.com", "Passw0rd!", "user")
    # Start background jobs (notifications)
    from .services.scheduler import start_scheduler
    start_scheduler()


@app.get("/")
def root():
    return {"status": "ok", "service": "financial-assistant-ai"}
