from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models import Transaction, TransactionType, TransactionStatus
from app.agents.financial_analyst import TransactionManagerAgent, FinancialAnalystAgent
from pydantic import BaseModel
import datetime

router = APIRouter()

class TransactionCreate(BaseModel):
    amount: float
    description: str
    type: TransactionType
    account_id: str
    date: datetime.datetime = None

class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    category: str
    type: TransactionType
    status: TransactionStatus
    date: datetime.datetime

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction and auto-categorize it"""
    try:
        # Initialize agents
        transaction_manager = TransactionManagerAgent()
        
        # Auto-categorize transaction
        transaction_data = {
            "amount": transaction.amount,
            "description": transaction.description,
            "type": transaction.type.value
        }
        
        category = transaction_manager.categorize_transaction(transaction_data)
        
        # Create transaction record
        db_transaction = Transaction(
            amount=transaction.amount,
            description=transaction.description,
            category=category,
            type=transaction.type,
            account_id=transaction.account_id,
            date=transaction.date or datetime.datetime.now()
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions/analysis")
async def analyze_transactions(db: Session = Depends(get_db)):
    """Get spending analysis using AI agents"""
    try:
        # Get recent transactions
        transactions = db.query(Transaction).all()
        transaction_data = [
            {
                "amount": t.amount,
                "description": t.description,
                "category": t.category,
                "type": t.type.value,
                "date": t.date.isoformat()
            }
            for t in transactions
        ]
        
        # Analyze with AI agent
        financial_analyst = FinancialAnalystAgent()
        analysis = financial_analyst.analyze_spending_patterns(transaction_data)
        
        return {
            "transactions_count": len(transactions),
            "analysis": analysis,
            "summary": {
                "total_income": sum(t.amount for t in transactions if t.type == TransactionType.INCOME),
                "total_expenses": sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE),
                "top_categories": get_top_categories(transactions)
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_top_categories(transactions: List[Transaction]) -> List[Dict]:
    """Helper function to get top spending categories"""
    expense_transactions = [t for t in transactions if t.type == TransactionType.EXPENSE]
    category_totals = {}
    
    for transaction in expense_transactions:
        category_totals[transaction.category] = category_totals.get(transaction.category, 0) + transaction.amount
    
    return [
        {"category": category, "total": total}
        for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
    ]