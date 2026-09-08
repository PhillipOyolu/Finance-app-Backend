from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app.models import User, Expense, Income, Category
from app.schemas import DashboardSummary, TransactionBase

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# Schema for the incoming POST payload from the modal
class TransactionCreatePayload(BaseModel):
    amount: float = Field(gt=0, description="Amount must be positive")
    description: str = Field(min_length=1)
    category_name: Optional[str] = "General"
    type: str = Field(pattern="^(income|expense)$")


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    current_year = now.year
    current_month = now.month

    # Total lifetime sums for balance calculation
    total_income = db.query(func.coalesce(func.sum(Income.amount), 0.0)).filter(
        Income.user_id == current_user.id
    ).scalar()

    total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0.0)).filter(
        Expense.user_id == current_user.id
    ).scalar()

    # Current month sums
    monthly_income = db.query(func.coalesce(func.sum(Income.amount), 0.0)).filter(
        Income.user_id == current_user.id,
        func.strftime("%Y", Income.created_at) == str(current_year),
        func.strftime("%m", Income.created_at) == f"{current_month:02d}"
    ).scalar()

    monthly_expense = db.query(func.coalesce(func.sum(Expense.amount), 0.0)).filter(
        Expense.user_id == current_user.id,
        func.strftime("%Y", Expense.created_at) == str(current_year),
        func.strftime("%m", Expense.created_at) == f"{current_month:02d}"
    ).scalar()

    # Fetch recent expenses and incomes (last 5 of each)
    recent_expenses = (
        db.query(Expense)
        .filter(Expense.user_id == current_user.id)
        .order_by(Expense.created_at.desc())
        .limit(5)
        .all()
    )

    recent_incomes = (
        db.query(Income)
        .filter(Income.user_id == current_user.id)
        .order_by(Income.created_at.desc())
        .limit(5)
        .all()
    )

    # Normalize into unified TransactionBase objects
    combined_txs = []

    for exp in recent_expenses:
        combined_txs.append(
            TransactionBase(
                id=exp.id,
                amount=exp.amount,
                description=exp.description or "Expense",
                category=exp.category.name if exp.category else "Expense",
                type="expense",
                date=exp.created_at,
            )
        )

    for inc in recent_incomes:
        combined_txs.append(
            TransactionBase(
                id=inc.id,
                amount=inc.amount,
                description=inc.description or "Income",
                category=inc.category.name if inc.category else "Income",
                type="income",
                date=inc.created_at,
            )
        )

    # Sort unified list chronologically descending and take top 5
    combined_txs.sort(key=lambda tx: tx.date, reverse=True)
    recent_five = combined_txs[:5]

    return {
        "total_balance": round(total_income - total_expense, 2),
        "monthly_income": round(monthly_income, 2),
        "monthly_expenses": round(monthly_expense, 2),
        "recent_transactions": recent_five,
    }


@router.post("/transaction", response_model=TransactionBase, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Match category by name (case-insensitive) to respect unique=True
    cat_name = payload.category_name.strip()
    category = db.query(Category).filter(
        func.lower(Category.name) == cat_name.lower()
    ).first()

    if not category:
        category = Category(name=cat_name, type=payload.type)
        db.add(category)
        db.flush()  # Assigns category.id without a full commit yet

    # 2. Use a timezone-naive UTC timestamp for SQLite stability
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    # 3. Create the respective Income or Expense record
    if payload.type == "expense":
        new_record = Expense(
            amount=payload.amount,
            description=payload.description.strip(),
            category_id=category.id,
            user_id=current_user.id,
            created_at=now_utc,
        )
    else:
        new_record = Income(
            amount=payload.amount,
            description=payload.description.strip(),
            category_id=category.id,
            user_id=current_user.id,
            created_at=now_utc,
        )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return TransactionBase(
        id=new_record.id,
        amount=new_record.amount,
        description=new_record.description,
        category=category.name,
        type=payload.type,
        date=new_record.created_at,
    )