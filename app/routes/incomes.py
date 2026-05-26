from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app import crud, schemas
from app.core.core_auth import get_current_user

router = APIRouter(
    prefix="/incomes",
    tags=["Incomes"]
)

@router.post("/", response_model=schemas.Income)
def create_income(
    income: schemas.IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_income(db, income, current_user.id)


@router.get("/", response_model=List[schemas.Income])
def read_incomes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_incomes(db, current_user.id)


@router.put("/{income_id}", response_model=schemas.Income)
def update_income(
    income_id: int,
    income: schemas.IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    existing = db.query(crud.Income).filter(
        crud.Income.id == income_id,
        crud.Income.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Income not found")

    return crud.update_income(db, income_id, income)


@router.delete("/{income_id}")
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    existing = db.query(crud.Income).filter(
        crud.Income.id == income_id,
        crud.Income.user_id == current_user.id
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Income not found")

    crud.delete_income(db, income_id)
    return {"message": "Income deleted successfully"}

