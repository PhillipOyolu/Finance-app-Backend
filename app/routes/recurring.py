from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.core_auth import get_current_user
from app import crud, schemas

router = APIRouter(prefix="/recurring", tags=["Recurring Transactions"])

@router.post("/", response_model=schemas.RecurringTransaction)
def create_recurring(data: schemas.RecurringTransactionCreate, 
                     db: Session = Depends(get_db),
                     user=Depends(get_current_user)):
    return crud.create_recurring_transaction(db, data, user.id)


@router.get("/", response_model=list[schemas.RecurringTransaction])
def list_recurring(db: Session = Depends(get_db),
                   user=Depends(get_current_user)):
    return crud.get_recurring_transactions(db, user.id)


@router.put("/{recurring_id}", response_model=schemas.RecurringTransaction)
def update_recurring(recurring_id: int,
                     data: schemas.RecurringTransactionCreate,
                     db: Session = Depends(get_db),
                     user=Depends(get_current_user)):
    return crud.update_recurring_transaction(db, recurring_id, data)


@router.delete("/{recurring_id}")
def delete_recurring(recurring_id: int,
                     db: Session = Depends(get_db),
                     user=Depends(get_current_user)):
    return crud.delete_recurring_transaction(db, recurring_id)


@router.post("/run")
def run_recurring(db: Session = Depends(get_db),
                  user=Depends(get_current_user)):
    return crud.run_due_recurring_transactions(db, user.id)
