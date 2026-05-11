from sqlalchemy.orm import Session
from app import models, schemas

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(
        name=expense.name,
        amount=expense.amount,
        category=expense.category
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session):
    return db.query(models.Expense).all()

def create_income(db: Session, income: schemas.IncomeCreate):
    db_income = models.Income(
        name=income.name,
        amount=income.amount,
        category=income.category
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income

def get_incomes(db: Session):
    return db.query(models.Income).all()

def update_expense(db: Session, expense_id: int, updated_data: schemas.ExpenseCreate):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        return None

    expense.name = updated_data.name
    expense.amount = updated_data.amount
    expense.category = updated_data.category

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

def update_income(db: Session, income_id: int, updated_data: schemas.IncomeCreate):
    income = db.query(models.Income).filter(models.Income.id == income_id).first()
    if not income:
        return None

    income.name = updated_data.name
    income.amount = updated_data.amount
    income.category = updated_data.category

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
