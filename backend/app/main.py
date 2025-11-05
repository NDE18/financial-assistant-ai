from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.api import transactions, categories, budgets, invoices, reports, analytics

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Assistant AI",
    description="Agentic AI-powered financial management system",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transactions.router, prefix=f"{settings.API_V1_PREFIX}/transactions", tags=["transactions"])
app.include_router(categories.router, prefix=f"{settings.API_V1_PREFIX}/categories", tags=["categories"])
app.include_router(budgets.router, prefix=f"{settings.API_V1_PREFIX}/budgets", tags=["budgets"])
app.include_router(invoices.router, prefix=f"{settings.API_V1_PREFIX}/invoices", tags=["invoices"])
app.include_router(reports.router, prefix=f"{settings.API_V1_PREFIX}/reports", tags=["reports"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_PREFIX}/analytics", tags=["analytics"])

@app.get("/")
def root():
    return {
        "message": "Financial Assistant AI API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
