from fastapi import FastAPI
from app.core.database import Base, engine
from app import models
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app import schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Finance app backend is running!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)

@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)

@app.post("/incomes/", response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return crud.create_income(db, income)

@app.get("/incomes/", response_model=list[schemas.Income])
def read_incomes(db: Session = Depends(get_db)):
    return crud.get_incomes(db)

@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    updated = crud.update_expense(db, expense_id, expense)
    if not updated:
        return {"error": "Expense not found"}
    return updated

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_expense(db, expense_id)
    if not deleted:
        return {"error": "Expense not found"}
    return {"message": "Expense deleted successfully"}

@app.put("/incomes/{income_id}", response_model=schemas.Income)
def update_income(income_id: int, income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    updated = crud.update_income(db, income_id, income)
    if not updated:
        return {"error": "Income not found"}
    return updated

@app.delete("/incomes/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_income(db, income_id)
    if not deleted:
        return {"error": "Income not found"}
    return {"message": "Income deleted successfully"}
