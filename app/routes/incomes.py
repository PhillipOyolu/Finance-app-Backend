from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app import crud, schemas
from app.core.core_auth import get_current_user

router = APIRouter(
    prefix="/incomes",
    tags=["Incomes"]
)

@router.post("/", response_model=schemas.Income, status_code=status.HTTP_201_CREATED)
def create_income(
    income: schemas.IncomeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_income(db, income, current_user.id)


@router.get("/", response_model=List[schemas.Income])
def read_incomes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_incomes(db, current_user.id, skip=skip, limit=limit)


@router.get("/{income_id}", response_model=schemas.Income)
def read_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    income = crud.get_income_by_id(db, income_id=income_id, user_id=current_user.id)
    if not income:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return income


@router.put("/{income_id}", response_model=schemas.Income)
def update_income(
    income_id: int,
    income: schemas.IncomeUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = crud.update_income(db, income_id=income_id, income_update=income, user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return updated


@router.delete("/{income_id}", status_code=status.HTTP_200_OK)
def delete_income(
    income_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_income(db, income_id=income_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Income not found")
    return {"message": "Income deleted successfully"}

