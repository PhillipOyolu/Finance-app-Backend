from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app.models import Expense, Income, Category, Budget

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

@router.get("/{year}/{month}")
def get_monthly_summary(
    year: int,
    month: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    if not (1 <= month <= 12):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Month must be between 1 and 12")

    # Portable date bounds
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    incomes = db.query(Income).filter(
        Income.user_id == current_user.id,
        Income.created_at >= start_date,
        Income.created_at < end_date
    ).all()

    expenses = db.query(Expense).filter(
        Expense.user_id == current_user.id,
        Expense.created_at >= start_date,
        Expense.created_at < end_date
    ).all()

    total_income = sum(i.amount for i in incomes)
    total_expenses = sum(e.amount for e in expenses)
    net = round(total_income - total_expenses, 2)

    categories = {c.id: c.name for c in db.query(Category).all()}

    income_by_category = {}
    for i in incomes:
        cat_name = categories.get(i.category_id, "Uncategorized")
        income_by_category[cat_name] = round(income_by_category.get(cat_name, 0.0) + i.amount, 2)

    expense_by_category = {}
    for e in expenses:
        cat_name = categories.get(e.category_id, "Uncategorized")
        expense_by_category[cat_name] = round(expense_by_category.get(cat_name, 0.0) + e.amount, 2)

    income_percentages = {
        cat: round((amt / total_income) * 100, 2)
        for cat, amt in income_by_category.items()
    } if total_income > 0 else {}

    expense_percentages = {
        cat: round((amt / total_expenses) * 100, 2)
        for cat, amt in expense_by_category.items()
    } if total_expenses > 0 else {}

    # Budgets for this month
    budgets = db.query(Budget).filter(
        Budget.user_id == current_user.id,
        Budget.month == month,
        Budget.year == year
    ).all()

    budget_summary = []
    for b in budgets:
        cat_name = categories.get(b.category_id, "Overall")
        spent = expense_by_category.get(cat_name, total_expenses if b.category_id is None else 0.0)
        remaining = round(b.amount - spent, 2)
        percent_used = round((spent / b.amount) * 100, 2) if b.amount > 0 else 0.0

        budget_summary.append({
            "budget_id": b.id,
            "category": cat_name,
            "limit": b.amount,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used
        })

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net": net,
        "income_by_category": income_by_category,
        "expense_by_category": expense_by_category,
        "income_percentages": income_percentages,
        "expense_percentages": expense_percentages,
        "budgets": budget_summary
    }
