from datetime import date, datetime
from typing import Optional, List
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app import models, schemas
from app.core import security


# ==============================================================================
# USER & AUTHENTICATION
# ==============================================================================

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_pwd = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ==============================================================================
# EXPENSES (TENANT ISOLATED)
# ==============================================================================

def get_expenses(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Expense]:
    return (
        db.query(models.Expense)
        .filter(models.Expense.user_id == user_id)
        .order_by(desc(models.Expense.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_expense_by_id(db: Session, expense_id: int, user_id: int) -> Optional[models.Expense]:
    return (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.user_id == user_id)
        .first()
    )


def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int) -> models.Expense:
    db_expense = models.Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(
    db: Session, expense_id: int, expense_update: schemas.ExpenseUpdate, user_id: int
) -> Optional[models.Expense]:
    db_expense = get_expense_by_id(db, expense_id=expense_id, user_id=user_id)
    if not db_expense:
        return None

    update_data = expense_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int, user_id: int) -> bool:
    db_expense = get_expense_by_id(db, expense_id=expense_id, user_id=user_id)
    if not db_expense:
        return False
    db.delete(db_expense)
    db.commit()
    return True


# ==============================================================================
# INCOMES (TENANT ISOLATED)
# ==============================================================================

def get_incomes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Income]:
    return (
        db.query(models.Income)
        .filter(models.Income.user_id == user_id)
        .order_by(desc(models.Income.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_income_by_id(db: Session, income_id: int, user_id: int) -> Optional[models.Income]:
    return (
        db.query(models.Income)
        .filter(models.Income.id == income_id, models.Income.user_id == user_id)
        .first()
    )


def create_income(db: Session, income: schemas.IncomeCreate, user_id: int) -> models.Income:
    db_income = models.Income(**income.model_dump(), user_id=user_id)
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


def update_income(
    db: Session, income_id: int, income_update: schemas.IncomeUpdate, user_id: int
) -> Optional[models.Income]:
    db_income = get_income_by_id(db, income_id=income_id, user_id=user_id)
    if not db_income:
        return None

    update_data = income_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_income, key, value)

    db.commit()
    db.refresh(db_income)
    return db_income


def delete_income(db: Session, income_id: int, user_id: int) -> bool:
    db_income = get_income_by_id(db, income_id=income_id, user_id=user_id)
    if not db_income:
        return False
    db.delete(db_income)
    db.commit()
    return True


# ==============================================================================
# CATEGORIES
# ==============================================================================

def get_categories(db: Session, type: Optional[str] = None) -> List[models.Category]:
    query = db.query(models.Category)
    if type:
        query = query.filter(models.Category.type == type)
    return query.all()


def get_category_by_id(db: Session, category_id: int) -> Optional[models.Category]:
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_category_by_name_and_type(db: Session, name: str, type: str) -> Optional[models.Category]:
    return db.query(models.Category).filter(
        models.Category.name == name,
        models.Category.type == type
    ).first()


def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ==============================================================================
# BUDGETS (TENANT ISOLATED + COMPOSITE KEY SCOPING)
# ==============================================================================

def get_budgets(db: Session, user_id: int, month: Optional[int] = None, year: Optional[int] = None) -> List[models.Budget]:
    query = db.query(models.Budget).filter(models.Budget.user_id == user_id)
    if month is not None:
        query = query.filter(models.Budget.month == month)
    if year is not None:
        query = query.filter(models.Budget.year == year)
    return query.all()


def get_budget_by_category_and_date(
    db: Session, user_id: int, category_id: Optional[int], month: int, year: int
) -> Optional[models.Budget]:
    return db.query(models.Budget).filter(
        models.Budget.user_id == user_id,
        models.Budget.category_id == category_id,
        models.Budget.month == month,
        models.Budget.year == year
    ).first()


def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int) -> models.Budget:
    db_budget = models.Budget(**budget.model_dump(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


def delete_budget(db: Session, budget_id: int, user_id: int) -> bool:
    db_budget = db.query(models.Budget).filter(
        models.Budget.id == budget_id,
        models.Budget.user_id == user_id
    ).first()
    if not db_budget:
        return False
    db.delete(db_budget)
    db.commit()
    return True


# ==============================================================================
# RECURRING TRANSACTIONS ENGINE
# ==============================================================================

def get_recurring_transactions(db: Session, user_id: int) -> List[models.RecurringTransaction]:
    return db.query(models.RecurringTransaction).filter(
        models.RecurringTransaction.user_id == user_id
    ).all()


def create_recurring_transaction(
    db: Session, recurring: schemas.RecurringTransactionCreate, user_id: int
) -> models.RecurringTransaction:
    db_recurring = models.RecurringTransaction(**recurring.model_dump(), user_id=user_id)
    db.add(db_recurring)
    db.commit()
    db.refresh(db_recurring)
    return db_recurring


def update_recurring_transaction(
    db: Session, recurring_id: int, update_data: schemas.RecurringTransactionUpdate, user_id: int
) -> Optional[models.RecurringTransaction]:
    db_rec = db.query(models.RecurringTransaction).filter(
        models.RecurringTransaction.id == recurring_id,
        models.RecurringTransaction.user_id == user_id
    ).first()
    if not db_rec:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(db_rec, key, value)

    db.commit()
    db.refresh(db_rec)
    return db_rec


def delete_recurring_transaction(db: Session, recurring_id: int, user_id: int) -> bool:
    db_rec = db.query(models.RecurringTransaction).filter(
        models.RecurringTransaction.id == recurring_id,
        models.RecurringTransaction.user_id == user_id
    ).first()
    if not db_rec:
        return False
    db.delete(db_rec)
    db.commit()
    return True


def run_due_recurring_transactions(db: Session, user_id: int) -> List[dict]:
    """
    Executes all recurring transactions whose next_run_date is <= today.
    Creates corresponding Expense/Income ledger entries and safely increments next_run_date.
    """
    today = date.today()
    due_items = db.query(models.RecurringTransaction).filter(
        models.RecurringTransaction.user_id == user_id,
        models.RecurringTransaction.active == True,
        models.RecurringTransaction.next_run_date <= today
    ).all()

    generated_transactions = []

    for item in due_items:
        # 1. Create the concrete ledger record
        if item.type == "expense":
            ledger_entry = models.Expense(
                amount=item.amount,
                description=f"[Recurring] {item.description or ''}".strip(),
                category_id=item.category_id,
                user_id=item.user_id
            )
            db.add(ledger_entry)
        elif item.type == "income":
            ledger_entry = models.Income(
                amount=item.amount,
                description=f"[Recurring] {item.description or ''}".strip(),
                category_id=item.category_id,
                user_id=item.user_id
            )
            db.add(ledger_entry)

        # 2. Advance next_run_date using calendar-safe date math
        if item.frequency == "weekly":
            item.next_run_date = item.next_run_date + relativedelta(weeks=1)
        elif item.frequency == "monthly":
            item.next_run_date = item.next_run_date + relativedelta(months=1)
        elif item.frequency == "yearly":
            item.next_run_date = item.next_run_date + relativedelta(years=1)

        generated_transactions.append({
            "recurring_id": item.id,
            "amount": item.amount,
            "type": item.type,
            "advanced_to": item.next_run_date
        })

    db.commit()
    return generated_transactions


# ==============================================================================
# SAVINGS GOALS (TENANT ISOLATED)
# ==============================================================================

def get_savings_goals(db: Session, user_id: int) -> List[models.SavingsGoal]:
    return db.query(models.SavingsGoal).filter(models.SavingsGoal.user_id == user_id).all()


def create_savings_goal(
    db: Session, goal: schemas.SavingsGoalCreate, user_id: int
) -> models.SavingsGoal:
    db_goal = models.SavingsGoal(**goal.model_dump(), user_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


def update_savings_goal(
    db: Session, goal_id: int, goal_update: schemas.SavingsGoalUpdate, user_id: int
) -> Optional[models.SavingsGoal]:
    db_goal = db.query(models.SavingsGoal).filter(
        models.SavingsGoal.id == goal_id,
        models.SavingsGoal.user_id == user_id
    ).first()
    if not db_goal:
        return None

    for key, value in goal_update.model_dump(exclude_unset=True).items():
        setattr(db_goal, key, value)

    db.commit()
    db.refresh(db_goal)
    return db_goal


def delete_savings_goal(db: Session, goal_id: int, user_id: int) -> bool:
    db_goal = db.query(models.SavingsGoal).filter(
        models.SavingsGoal.id == goal_id,
        models.SavingsGoal.user_id == user_id
    ).first()
    if not db_goal:
        return False
    db.delete(db_goal)
    db.commit()
    return True