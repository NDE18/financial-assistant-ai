from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.report import Report
from app.models.transaction import Transaction
from app.schemas.report import ReportCreate, ReportResponse
from app.agents.orchestrator import OrchestratorAgent
import json

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=201)
async def create_report(
    report: ReportCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Generate a financial report"""
    
    # Create report record
    db_report = Report(
        title=report.title,
        type=report.type,
        start_date=report.start_date,
        end_date=report.end_date,
        status="generating"
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # Background report generation
    background_tasks.add_task(
        generate_report_async,
        db_report.id,
        report.dict()
    )
    
    return db_report

async def generate_report_async(report_id: int, report_data: dict):
    """Background task to generate report"""
    from app.database import SessionLocal
    
    db = SessionLocal()
    try:
        # Get transactions for period
        transactions = db.query(Transaction).filter(
            Transaction.date >= report_data['start_date'],
            Transaction.date <= report_data['end_date']
        ).all()
        
        # Prepare data
        transaction_data = [
            {
                'date': t.date.isoformat(),
                'description': t.description,
                'amount': t.amount,
                'type': t.type,
                'category': t.category.name if t.category else None
            }
            for t in transactions
        ]
        
        # Generate report using AI
        orchestrator = OrchestratorAgent()
        crew = orchestrator.generate_comprehensive_report_workflow({
            'transactions': transaction_data,
            'period': report_data['type'],
            'start_date': report_data['start_date'],
            'end_date': report_data['end_date']
        })
        
        result = crew.kickoff()
        report_content = json.loads(result)
        
        # Update report
        report = db.query(Report).filter(Report.id == report_id).first()
        if report:
            report.summary = report_content.get('summary')
            report.insights = json.dumps(report_content.get('insights', []))
            report.recommendations = json.dumps(report_content.get('recommendations', []))
            report.status = "completed"
            report.completed_at = datetime.utcnow()
            
            db.commit()
    except Exception as e:
        report = db.query(Report).filter(Report.id == report_id).first()
        if report:
            report.status = "failed"
            db.commit()
    finally:
        db.close()

@router.get("/", response_model=List[ReportResponse])
def get_reports(
    skip: int = 0,
    limit: int = 50,
    type: str = None,
    db: Session = Depends(get_db)
):
    """Get all reports"""
    
    query = db.query(Report)
    if type:
        query = query.filter(Report.type == type)
    
    reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get report by ID"""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return report

@router.delete("/{report_id}", status_code=204)
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete report"""
    
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    
    return None