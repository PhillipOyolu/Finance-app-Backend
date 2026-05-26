from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models import User, Expense, Income, Category
from app.core.security import hash_password
from app.models import Budget

# Expense CRUD

def create_expense(db: Session, expense, user_id: int):
    db_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        category_id=expense.category_id,
        user_id=user_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()


def update_expense(db: Session, expense_id: int, updated_data):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return None

    expense.amount = updated_data.amount
    expense.description = updated_data.description
    expense.category_id = updated_data.category_id

    db.commit()
    db.refresh(expense)
    return expense


def delete_expense(db: Session, expense_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        return None

    db.delete(expense)
    db.commit()
    return True


def get_expenses_by_month(db: Session, year: int, month: int, user_id: int):
    return db.query(Expense).filter(
        Expense.user_id == user_id,
        extract('year', Expense.created_at) == year,
        extract('month', Expense.created_at) == month
    ).all()


# Income CRUD

def create_income(db: Session, income, user_id: int):
    db_income = Income(
        amount=income.amount,
        description=income.description,
        category_id=income.category_id,
        user_id=user_id
    )
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def get_incomes(db: Session, user_id: int):
    return db.query(Income).filter(Income.user_id == user_id).all()


def update_income(db: Session, income_id: int, updated_data):
    income = db.query(Income).filter(Income.id == income_id).first()
    if not income:
        return None

    income.amount = updated_data.amount
    income.description = updated_data.description
    income.category_id = updated_data.category_id

    db.commit()
    db.refresh(income)
    return income


def delete_income(db: Session, income_id: int):
    income = db.query(Income).filter(Income.id == income_id).first()
    if not income:
        return None

    db.delete(income)
    db.commit()
    return True


def get_incomes_by_month(db: Session, year: int, month: int, user_id: int):
    return db.query(Income).filter(
        Income.user_id == user_id,
        extract('year', Income.created_at) == year,
        extract('month', Income.created_at) == month
    ).all()

# Category CRUD

def create_category(db: Session, category):
    db_category = Category(
        name=category.name,
        type=category.type
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_map(db: Session):
    categories = db.query(Category).all()
    return {c.id: c.name for c in categories}


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

# Budget CRUD

def create_budget(db: Session, budget, user_id: int):
    db_budget = Budget(
        amount=budget.amount,
        month=budget.month,
        year=budget.year,
        category_id=budget.category_id,
        user_id=user_id
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budgets(db: Session, user_id: int, month: int, year: int):
    return db.query(Budget).filter(
        Budget.user_id == user_id,
        Budget.month == month,
        Budget.year == year
    ).all()

# User CRUD

def create_user(db: Session, user):
    hashed = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
