from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud, schemas

router = APIRouter(
    prefix="/budgets",
    tags=["Budgets"]
)

@router.post("/", response_model=schemas.Budget)
def create_budget(
    budget: schemas.BudgetCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_budget(db, budget, current_user.id)


@router.get("/{year}/{month}", response_model=List[schemas.Budget])
def get_budgets(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_budgets(db, current_user.id, month, year)
