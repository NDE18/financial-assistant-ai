from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import (
    TransactionCreate, 
    TransactionUpdate, 
    TransactionResponse
)
from app.agents.orchestrator import OrchestratorAgent
import json

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    transaction: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create a new transaction with AI classification"""
    
    # Create transaction
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Background AI classification
    background_tasks.add_task(
        classify_transaction_async,
        db_transaction.id,
        transaction.dict()
    )
    
    return format_transaction_response(db_transaction, db)

async def classify_transaction_async(transaction_id: int, transaction_data: dict):
    """Background task to classify transaction using AI"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        orchestrator = OrchestratorAgent()
        classifier = orchestrator.classifier
        
        # Run classification
        task = classifier.classify_transaction(transaction_data)
        crew = Crew(
            agents=[classifier.create_agent()],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()
        
        # Parse result
        classification = json.loads(result)
        
        # Update transaction
        transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if transaction:
            # Find or create category
            category = db.query(Category).filter(
                Category.name == classification['category']
            ).first()
            
            if category:
                transaction.category_id = category.id
            
            transaction.tags = json.dumps(classification.get('tags', []))
            transaction.is_recurring = classification.get('is_recurring', False)
            transaction.confidence_score = classification.get('confidence_score', 0.0)
            transaction.notes = classification.get('notes', '')
            
            db.commit()
    finally:
        db.close()

@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get transactions with filters"""
    
    query = db.query(Transaction)
    
    if type:
        query = query.filter(Transaction.type == type)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    
    return [format_transaction_response(t, db) for t in transactions]

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Get transaction by ID"""
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return format_transaction_response(transaction, db)

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: Session = Depends(get_db)
):
    """Update transaction"""
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for key, value in transaction_update.dict(exclude_unset=True).items():
        setattr(transaction, key, value)
    
    db.commit()
    db.refresh(transaction)
    
    return format_transaction_response(transaction, db)

@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """Delete transaction"""
    
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    
    return None

@router.post("/batch", response_model=List[TransactionResponse])
async def create_transactions_batch(
    transactions: List[TransactionCreate],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create multiple transactions with batch AI classification"""
    
    created_transactions = []
    for transaction_data in transactions:
        db_transaction = Transaction(**transaction_data.dict())
        db.add(db_transaction)
        created_transactions.append(db_transaction)
    
    db.commit()
    
    # Background batch classification
    background_tasks.add_task(
        classify_transactions_batch,
        [t.id for t in created_transactions],
        [t.dict() for t in transactions]
    )
    
    return [format_transaction_response(t, db) for t in created_transactions]

async def classify_transactions_batch(transaction_ids: List[int], transactions_data: List[dict]):
    """Background task for batch classification"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        orchestrator = OrchestratorAgent()
        crew = orchestrator.process_transactions_workflow(transactions_data)
        result = crew.kickoff()
        
        # Update transactions with classifications
        classifications = json.loads(result)
        
        for tid, classification in zip(transaction_ids, classifications):
            transaction = db.query(Transaction).filter(Transaction.id == tid).first()
            if transaction and classification:
                category = db.query(Category).filter(
                    Category.name == classification['category']
                ).first()
                
                if category:
                    transaction.category_id = category.id
                
                transaction.tags = json.dumps(classification.get('tags', []))
                transaction.is_recurring = classification.get('is_recurring', False)
                transaction.confidence_score = classification.get('confidence_score', 0.0)
        
        db.commit()
    finally:
        db.close()

def format_transaction_response(transaction: Transaction, db: Session) -> dict:
    """Format transaction with category name"""
    response = TransactionResponse.from_orm(transaction)
    if transaction.category:
        response.category_name = transaction.category.name
    return response