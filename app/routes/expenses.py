from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app import crud, schemas
from app.core.core_auth import get_current_user

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)

@router.post("/", response_model=schemas.Expense)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_expense(db, expense, current_user.id)


@router.get("/", response_model=List[schemas.Expense])
def read_expenses(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_expenses(db, current_user.id)


@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Ensure the expense belongs to the user
    existing = db.query(crud.Expense).filter(
        crud.Expense.id == expense_id,
        crud.Expense.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    return crud.update_expense(db, expense_id, expense)


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Ensure the expense belongs to the user
    existing = db.query(crud.Expense).filter(
        crud.Expense.id == expense_id,
        crud.Expense.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    crud.delete_expense(db, expense_id)
    return {"message": "Expense deleted successfully"}

