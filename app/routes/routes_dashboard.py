from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app.models import User, Expense, Income, Category
from app import schemas

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

class QuickTransactionCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be positive")
    description: str = Field(min_length=1, max_length=255)
    category_name: Optional[str] = Field("General", max_length=50)
    type: schemas.TransactionTypeEnum


@router.get("/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)
    start_of_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    
    # Calculate end of month
    if now.month == 12:
        start_of_next_month = datetime(now.year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        start_of_next_month = datetime(now.year, now.month + 1, 1, tzinfo=timezone.utc)

    # Total lifetime sums
    total_income = db.query(func.coalesce(func.sum(Income.amount), 0.0)).filter(
        Income.user_id == current_user.id
    ).scalar()

    total_expense = db.query(func.coalesce(func.sum(Expense.amount), 0.0)).filter(
        Expense.user_id == current_user.id
    ).scalar()

    # Current month sums using portable date boundaries
    monthly_income = db.query(func.coalesce(func.sum(Income.amount), 0.0)).filter(
        Income.user_id == current_user.id,
        Income.created_at >= start_of_month,
        Income.created_at < start_of_next_month
    ).scalar()

    monthly_expense = db.query(func.coalesce(func.sum(Expense.amount), 0.0)).filter(
        Expense.user_id == current_user.id,
        Expense.created_at >= start_of_month,
        Expense.created_at < start_of_next_month
    ).scalar()

    # Last 5 records of each
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

    combined_txs = []
    for exp in recent_expenses:
        combined_txs.append(
            schemas.TransactionRead(
                id=exp.id,
                amount=exp.amount,
                description=exp.description,
                category_name=exp.category.name if exp.category else "Expense",
                type=schemas.TransactionTypeEnum.EXPENSE,
                date=exp.created_at,
            )
        )

    for inc in recent_incomes:
        combined_txs.append(
            schemas.TransactionRead(
                id=inc.id,
                amount=inc.amount,
                description=inc.description,
                category_name=inc.category.name if inc.category else "Income",
                type=schemas.TransactionTypeEnum.INCOME,
                date=inc.created_at,
            )
        )

    combined_txs.sort(key=lambda tx: tx.date, reverse=True)

    return schemas.DashboardSummary(
        total_balance=round(float(total_income - total_expense), 2),
        monthly_income=round(float(monthly_income), 2),
        monthly_expenses=round(float(monthly_expense), 2),
        recent_transactions=combined_txs[:5]
    )


@router.post("/transaction", response_model=schemas.TransactionRead, status_code=status.HTTP_201_CREATED)
def create_quick_transaction(
    payload: QuickTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cat_name = (payload.category_name or "General").strip()
    category = db.query(Category).filter(
        func.lower(Category.name) == cat_name.lower(),
        Category.type == payload.type.value
    ).first()

    if not category:
        category = Category(name=cat_name, type=payload.type.value)
        db.add(category)
        db.flush()

    if payload.type == schemas.TransactionTypeEnum.EXPENSE:
        new_record = Expense(
            amount=payload.amount,
            description=payload.description.strip(),
            category_id=category.id,
            user_id=current_user.id
        )
    else:
        new_record = Income(
            amount=payload.amount,
            description=payload.description.strip(),
            category_id=category.id,
            user_id=current_user.id
        )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return schemas.TransactionRead(
        id=new_record.id,
        amount=new_record.amount,
        description=new_record.description,
        category_name=category.name,
        type=payload.type,
        date=new_record.created_at
    )