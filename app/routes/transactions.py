from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date, datetime, time

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app.models import Expense, Income
from app import schemas

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.get("/filter", response_model=List[schemas.TransactionRead])
def filter_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category_id: Optional[int] = None,
    min_amount: Optional[float] = Query(None, gt=0),
    max_amount: Optional[float] = Query(None, gt=0),
    type: Optional[schemas.TransactionTypeEnum] = None,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results: List[schemas.TransactionRead] = []

    # 1. Fetch Expenses (only if not restricted to 'income')
    if type is None or type == schemas.TransactionTypeEnum.EXPENSE:
        eq = db.query(Expense).filter(Expense.user_id == current_user.id)
        if start_date:
            eq = eq.filter(Expense.created_at >= datetime.combine(start_date, time.min))
        if end_date:
            eq = eq.filter(Expense.created_at <= datetime.combine(end_date, time.max))
        if category_id:
            eq = eq.filter(Expense.category_id == category_id)
        if min_amount is not None:
            eq = eq.filter(Expense.amount >= min_amount)
        if max_amount is not None:
            eq = eq.filter(Expense.amount <= max_amount)

        for e in eq.all():
            results.append(schemas.TransactionRead(
                id=e.id,
                amount=e.amount,
                description=e.description,
                category_name=e.category.name if e.category else "Uncategorized",
                type=schemas.TransactionTypeEnum.EXPENSE,
                date=e.created_at
            ))

    # 2. Fetch Incomes (only if not restricted to 'expense')
    if type is None or type == schemas.TransactionTypeEnum.INCOME:
        iq = db.query(Income).filter(Income.user_id == current_user.id)
        if start_date:
            iq = iq.filter(Income.created_at >= datetime.combine(start_date, time.min))
        if end_date:
            iq = iq.filter(Income.created_at <= datetime.combine(end_date, time.max))
        if category_id:
            iq = iq.filter(Income.category_id == category_id)
        if min_amount is not None:
            iq = iq.filter(Income.amount >= min_amount)
        if max_amount is not None:
            iq = iq.filter(Income.amount <= max_amount)

        for i in iq.all():
            results.append(schemas.TransactionRead(
                id=i.id,
                amount=i.amount,
                description=i.description,
                category_name=i.category.name if i.category else "Uncategorized",
                type=schemas.TransactionTypeEnum.INCOME,
                date=i.created_at
            ))

    # 3. Sort descending by date and apply pagination
    results.sort(key=lambda x: x.date, reverse=True)
    return results[skip : skip + limit]

