from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud

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
):
    incomes = crud.get_incomes_by_month(db, year, month, current_user.id)
    expenses = crud.get_expenses_by_month(db, year, month, current_user.id)

    if not incomes and not expenses:
        return {"message": "No data found for this month"}

    total_income = sum(i.amount for i in incomes)
    total_expenses = sum(e.amount for e in expenses)
    net = total_income - total_expenses

    category_map = crud.get_category_map(db)

    # Group income by category
    income_by_category = {}
    for i in incomes:
        cat_name = category_map.get(i.category_id, "Uncategorised")
        income_by_category[cat_name] = income_by_category.get(cat_name, 0) + i.amount

    # Group expenses by category
    expense_by_category = {}
    for e in expenses:
        cat_name = category_map.get(e.category_id, "Uncategorised")
        expense_by_category[cat_name] = expense_by_category.get(cat_name, 0) + e.amount

    # Percentages
    income_percentages = {
        cat: round((amount / total_income) * 100, 2)
        for cat, amount in income_by_category.items()
    } if total_income > 0 else {}

    expense_percentages = {
        cat: round((amount / total_expenses) * 100, 2)
        for cat, amount in expense_by_category.items()
    } if total_expenses > 0 else {}

    # Budgets
    budgets = crud.get_budgets(db, current_user.id, month, year)

    budget_summary = []

    for b in budgets:
        if b.category_id:
            category_name = category_map.get(b.category_id, "Uncategorised")
            spent = expense_by_category.get(category_name, 0)
        else:
            spent = total_expenses

        remaining = b.amount - spent
        percent_used = round((spent / b.amount) * 100, 2) if b.amount > 0 else 0

        budget_summary.append({
            "budget_id": b.id,
            "category": category_map.get(b.category_id, "Overall"),
            "limit": b.amount,
            "spent": spent,
            "remaining": remaining,
            "percent_used": percent_used
        })

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net": net,
        "income_by_category": income_by_category,
        "expense_by_category": expense_by_category,
        "income_percentages": income_percentages,
        "expense_percentages": expense_percentages,
        "income_entries": incomes,
        "expense_entries": expenses,
        "budgets": budget_summary
    }

# Yearly Summary

@router.get("/yearly")
def yearly_summary(year: int,
                   db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    return crud.get_yearly_summary(db, user.id, year)
