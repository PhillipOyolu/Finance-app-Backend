from sqlalchemy.orm import Session
from sqlalchemy import extract
from app import models, schemas

# Expense CRUD

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        name=expense.name,
        amount=expense.amount,
        category=expense.category,
        category_id=expense.category_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session):
    return db.query(models.Expense).all()

def update_expense(db: Session, expense_id: int, updated_data: schemas.ExpenseCreate):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None

    expense.name = updated_data.name
    expense.amount = updated_data.amount
    expense.category = updated_data.category
    expense.category_id = updated_data.category_id

    db.commit()
    db.refresh(expense)
    return expense

def delete_expense(db: Session, expense_id: int):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None

    db.delete(expense)
    db.commit()
    return True

# Income CRUD

def create_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.Income(
        name=income.name,
        amount=income.amount,
        category=income.category,
        category_id=income.category_id
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

def get_incomes(db: Session):
    return db.query(models.Income).all()

def update_income(db: Session, income_id: int, updated_data: schemas.IncomeCreate):
    income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not income:
        return None

    income.name = updated_data.name
    income.amount = updated_data.amount
    income.category = updated_data.category
    income.category_id = updated_data.category_id

    db.commit()
    db.refresh(income)
    return income

def delete_income(db: Session, income_id: int):
    income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not income:
        return None

    db.delete(income)
    db.commit()
    return True

# Monthly Summary Helpers

def get_incomes_by_month(db: Session, year: int, month: int):
    return db.query(models.Income).filter(
        extract('year', models.Income.created_at) == year,
        extract('month', models.Income.created_at) == month
    ).all()

def get_expenses_by_month(db: Session, year: int, month: int):
    return db.query(models.Expense).filter(
        extract('year', models.Expense.created_at) == year,
        extract('month', models.Expense.created_at) == month
    ).all()

# Category CRUD

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(
        name=category.name,
        type=category.type
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

def get_category_map(db: Session):
    categories = db.query(models.Category).all()
    return {c.id: c.name for c in categories}

def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False
