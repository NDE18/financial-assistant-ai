from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.budget import Budget
from app.schemas.analytics import (
    AnalyticsResponse,
    KPIData,
    CategoryBreakdown,
    TrendData
)

router = APIRouter()

@router.get("/dashboard", response_model=AnalyticsResponse)
async def get_dashboard_analytics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard analytics"""
    
    # Default to last 30 days
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=30)
    
    # Get transactions for period
    transactions = db.query(Transaction).filter(
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    # Calculate KPIs
    kpis = calculate_kpis(transactions)
    
    # Category breakdown
    category_breakdown = calculate_category_breakdown(transactions, db)
    
    # Trends
    trends = calculate_trends(transactions, start_date, end_date)
    
    # Generate insights
    insights = generate_insights(transactions, kpis, category_breakdown)
    
    # Check for alerts
    alerts = check_alerts(transactions, db)
    
    return AnalyticsResponse(
        period_start=start_date,
        period_end=end_date,
        kpis=kpis,
        category_breakdown=category_breakdown,
        trends=trends,
        insights=insights,
        alerts=alerts
    )

def calculate_kpis(transactions: List[Transaction]) -> KPIData:
    """Calculate key performance indicators"""
    
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_balance = total_income - total_expenses
    
    savings_rate = (net_balance / total_income * 100) if total_income > 0 else 0
    
    # Find largest transactions
    expenses = [t for t in transactions if t.type == 'expense']
    incomes = [t for t in transactions if t.type == 'income']
    
    largest_expense = None
    if expenses:
        largest = max(expenses, key=lambda t: t.amount)
        largest_expense = {
            'description': largest.description,
            'amount': largest.amount,
            'date': largest.date.isoformat()
        }
    
    largest_income = None
    if incomes:
        largest = max(incomes, key=lambda t: t.amount)
        largest_income = {
            'description': largest.description,
            'amount': largest.amount,
            'date': largest.date.isoformat()
        }
    
    return KPIData(
        total_income=total_income,
        total_expenses=total_expenses,
        net_balance=net_balance,
        savings_rate=round(savings_rate, 2),
        largest_expense=largest_expense,
        largest_income=largest_income
    )

def calculate_category_breakdown(
    transactions: List[Transaction],
    db: Session
) -> List[CategoryBreakdown]:
    """Calculate spending by category"""
    
    category_data = defaultdict(lambda: {'amount': 0, 'count': 0})
    
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    for t in transactions:
        if t.type == 'expense' and t.category:
            category_data[t.category.name]['amount'] += t.amount
            category_data[t.category.name]['count'] += 1
    
    breakdown = []
    for category, data in category_data.items():
        percentage = (data['amount'] / total_expenses * 100) if total_expenses > 0 else 0
        breakdown.append(CategoryBreakdown(
            category=category,
            amount=data['amount'],
            percentage=round(percentage, 2),
            transaction_count=data['count']
        ))
    
    # Sort by amount descending
    breakdown.sort(key=lambda x: x.amount, reverse=True)
    
    return breakdown

def calculate_trends(
    transactions: List[Transaction],
    start_date: datetime,
    end_date: datetime
) -> List[TrendData]:
    """Calculate daily/weekly trends"""
    
    # Group by date
    daily_data = defaultdict(lambda: {'income': 0, 'expenses': 0})
    
    for t in transactions:
        date_key = t.date.strftime('%Y-%m-%d')
        if t.type == 'income':
            daily_data[date_key]['income'] += t.amount
        else:
            daily_data[date_key]['expenses'] += t.amount
    
    trends = []
    current_date = start_date
    running_balance = 0
    
    while current_date <= end_date:
        date_key = current_date.strftime('%Y-%m-%d')
        data = daily_data.get(date_key, {'income': 0, 'expenses': 0})
        
        running_balance += data['income'] - data['expenses']
        
        trends.append(TrendData(
            date=date_key,
            income=data['income'],
            expenses=data['expenses'],
            balance=running_balance
        ))
        
        current_date += timedelta(days=1)
    
    return trends

def generate_insights(
    transactions: List[Transaction],
    kpis: KPIData,
    category_breakdown: List[CategoryBreakdown]
) -> List[str]:
    """Generate AI-powered insights"""
    
    insights = []
    
    # Savings rate insight
    if kpis.savings_rate > 20:
        insights.append(f"Excellent! Your savings rate is {kpis.savings_rate}%, well above the recommended 20%.")
    elif kpis.savings_rate > 10:
        insights.append(f"Good job! You're saving {kpis.savings_rate}% of your income.")
    else:
        insights.append(f"Consider increasing your savings. Current rate: {kpis.savings_rate}%.")
    
    # Top spending category
    if category_breakdown:
        top_category = category_breakdown[0]
        if top_category.percentage > 30:
            insights.append(
                f"{top_category.category} accounts for {top_category.percentage}% of expenses. "
                f"Consider reviewing this category for savings opportunities."
            )
    
    # Balance insight
    if kpis.net_balance < 0:
        insights.append(
            f"Alert: You spent ${abs(kpis.net_balance):.2f} more than you earned this period."
        )
    
    # Transaction count
    expense_count = sum(cb.transaction_count for cb in category_breakdown)
    if expense_count > 100:
        insights.append(
            f"You made {expense_count} expense transactions. Consider consolidating purchases to reduce fees."
        )
    
    return insights

def check_alerts(transactions: List[Transaction], db: Session) -> List[str]:
    """Check for budget alerts and anomalies"""
    
    alerts = []
    
    # Check budget overruns
    budgets = db.query(Budget).filter(
        Budget.end_date >= datetime.utcnow()
    ).all()
    
    for budget in budgets:
        if budget.is_exceeded:
            alerts.append(
                f"Budget Alert: {budget.name} is {((budget.spent/budget.amount - 1) * 100):.0f}% over budget!"
            )
        elif budget.spent / budget.amount > budget.alert_threshold:
            percentage = (budget.spent / budget.amount * 100)
            alerts.append(
                f"Warning: {budget.name} is at {percentage:.0f}% of budget."
            )
    
    # Check for large transactions
    avg_expense = sum(t.amount for t in transactions if t.type == 'expense') / max(len([t for t in transactions if t.type == 'expense']), 1)
    
    for t in transactions:
        if t.type == 'expense' and t.amount > avg_expense * 3:
            alerts.append(
                f"Unusual transaction detected: ${t.amount:.2f} for {t.description}"
            )
    
    return alerts

@router.get("/categories/{category_id}/analysis")
async def get_category_analysis(
    category_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get detailed analysis for a specific category"""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Default to last 90 days
    if not end_date:
        end_date = datetime.utcnow()
    if not start_date:
        start_date = end_date - timedelta(days=90)
    
    # Get transactions
    transactions = db.query(Transaction).filter(
        Transaction.category_id == category_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    
    # Analysis
    total_spent = sum(t.amount for t in transactions)
    avg_transaction = total_spent / len(transactions) if transactions else 0
    
    # Monthly breakdown
    monthly_spending = defaultdict(float)
    for t in transactions:
        month_key = t.date.strftime('%Y-%m')
        monthly_spending[month_key] += t.amount
    
    return {
        'category': category.name,
        'period': {
            'start': start_date.isoformat(),
            'end': end_date.isoformat()
        },
        'summary': {
            'total_spent': total_spent,
            'transaction_count': len(transactions),
            'average_transaction': round(avg_transaction, 2),
            'largest_transaction': max((t.amount for t in transactions), default=0)
        },
        'monthly_breakdown': dict(monthly_spending),
        'budget': {
            'monthly_budget': category.monthly_budget,
            'average_monthly_spent': total_spent / 3 if transactions else 0  # 90 days = ~3 months
        }
    }