from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app.models import Expense, Income

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("/filter")
def filter_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    type: Optional[str] = None,  # "income", "expense", or None
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Start queries filtered by user
    expense_query = db.query(Expense).filter(Expense.user_id == current_user.id)
    income_query = db.query(Income).filter(Income.user_id == current_user.id)

    # Apply filters
    if start_date:
        expense_query = expense_query.filter(Expense.created_at >= start_date)
        income_query = income_query.filter(Income.created_at >= start_date)

    if end_date:
        expense_query = expense_query.filter(Expense.created_at <= end_date)
        income_query = income_query.filter(Income.created_at <= end_date)

    if category_id:
        expense_query = expense_query.filter(Expense.category_id == category_id)
        income_query = income_query.filter(Income.category_id == category_id)

    if min_amount:
        expense_query = expense_query.filter(Expense.amount >= min_amount)
        income_query = income_query.filter(Income.amount >= min_amount)

    if max_amount:
        expense_query = expense_query.filter(Expense.amount <= max_amount)
        income_query = income_query.filter(Income.amount <= max_amount)

    # Fetch results
    expenses = expense_query.all()
    incomes = income_query.all()

    # Apply type filter AFTER fetching
    if type == "expense":
        incomes = []
    elif type == "income":
        expenses = []

    # Combine and sort by date
    combined = expenses + incomes
    combined.sort(key=lambda x: x.created_at, reverse=True)

    return combined

