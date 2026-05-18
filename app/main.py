from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app import models, schemas, crud

# Database Initialization

Base.metadata.create_all(bind=engine)

# FastAPI App Instance

app = FastAPI()

# Root Endpoint

@app.get("/")
def root():
    return {"message": "Finance app backend is running!"}

# Expense Routes

@app.post("/expenses/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)

@app.get("/expenses/", response_model=list[schemas.Expense])
def read_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)

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

# Income Routes

@app.post("/incomes/", response_model=schemas.Income)
def create_income(income: schemas.IncomeCreate, db: Session = Depends(get_db)):
    return crud.create_income(db, income)

@app.get("/incomes/", response_model=list[schemas.Income])
def read_incomes(db: Session = Depends(get_db)):
    return crud.get_incomes(db)

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

# Monthly Summary Route

@app.get("/summary/{year}/{month}")
def get_monthly_summary(year: int, month: int, db: Session = Depends(get_db)):
    incomes = crud.get_incomes_by_month(db, year, month)
    expenses = crud.get_expenses_by_month(db, year, month)

    total_income = sum(i.amount for i in incomes)
    total_expenses = sum(e.amount for e in expenses)
    net = total_income - total_expenses

    # Fetch category map once
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

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net": net,
        "income_by_category": income_by_category,
        "expense_by_category": expense_by_category,
        "income_percentages": income_percentages,
        "expense_percentages": expense_percentages,
        "income_entries": incomes,
        "expense_entries": expenses
    }

# Category Routes

@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.get("/categories/", response_model=list[schemas.Category])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_category(db, category_id)
    if not deleted:
        return {"error": "Category not found"}
    return {"message": "Category deleted successfully"}
