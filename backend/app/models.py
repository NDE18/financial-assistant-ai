from __future__ import annotations
from datetime import date, datetime
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel


class Direction(str, Enum):
    expense = "expense"
    income = "income"


class InvoiceType(str, Enum):
    payable = "payable"
    receivable = "receivable"


class ReportType(str, Enum):
    balance_sheet = "balance_sheet"
    income_statement = "income_statement"
    cashflow = "cashflow"


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    institution: Optional[str] = None
    currency: str = "EUR"
    current_balance: float = 0.0


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    account_id: Optional[int] = Field(default=None, foreign_key="account.id")
    date: date
    amount: float
    direction: Direction
    category: Optional[str] = None
    description: Optional[str] = None
    status: str = "booked"  # booked, pending, disputed
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: InvoiceType
    due_date: date
    amount: float
    currency: str = "EUR"
    status: str = "open"  # open, paid, overdue, canceled
    counterparty: Optional[str] = None  # vendor/customer
    file_path: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Budget(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    period: str = "monthly"
    start_date: date
    end_date: date
    total_amount: float


class BudgetLine(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    budget_id: int = Field(foreign_key="budget.id")
    category: str
    limit_amount: float
    spent_amount: float = 0.0


class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: Optional[str] = None
    original_filename: str
    stored_path: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")


class ReconciliationMatch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bank_ref: str
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id")
    status: str = "unmatched"  # matched, partial, unmatched
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    severity: str = "info"  # info, warning, critical
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved: bool = False


class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: ReportType
    period_start: date
    period_end: date
    content_json: str  # JSON string storing the report content/metrics
    created_at: datetime = Field(default_factory=datetime.utcnow)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    hashed_password: str
    is_active: bool = True
    role: str = "user"  # 'admin' or 'user'


class ExchangeRate(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    currency: str  # e.g. "USD"
    date: date
    rate_to_base: float  # how many BASE currency units for 1 unit of currency
