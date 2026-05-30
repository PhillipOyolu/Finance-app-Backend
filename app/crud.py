from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import date, timedelta
from app.models import User, Expense, Income, Category, Budget, RecurringTransaction, SavingsGoal
from app.core.security import hash_password
from app import schemas

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

# Recurring Transactions CRUD

def create_recurring_transaction(db: Session, data, user_id: int):
    recurring = RecurringTransaction(
        amount=data.amount,
        description=data.description,
        category_id=data.category_id,
        type=data.type,
        frequency=data.frequency,
        next_run_date=data.next_run_date,
        active=data.active,
        user_id=user_id
    )
    db.add(recurring)
    db.commit()
    db.refresh(recurring)
    return recurring

def get_recurring_transactions(db: Session, user_id: int):
    return db.query(RecurringTransaction).filter(
        RecurringTransaction.user_id == user_id
    ).all()

def update_recurring_transaction(db: Session, recurring_id: int, updated_data):
    recurring = db.query(RecurringTransaction).filter(
        RecurringTransaction.id == recurring_id
    ).first()

    if not recurring:
        return None

    recurring.amount = updated_data.amount
    recurring.description = updated_data.description
    recurring.category_id = updated_data.category_id
    recurring.type = updated_data.type
    recurring.frequency = updated_data.frequency
    recurring.next_run_date = updated_data.next_run_date
    recurring.active = updated_data.active

    db.commit()
    db.refresh(recurring)
    return recurring

def delete_recurring_transaction(db: Session, recurring_id: int):
    recurring = db.query(RecurringTransaction).filter(
        RecurringTransaction.id == recurring_id
    ).first()

    if not recurring:
        return None

    db.delete(recurring)
    db.commit()
    return True

# Auto-generation Logic CRUD

def run_due_recurring_transactions(db: Session, user_id: int):
    today = date.today()

    due_items = db.query(RecurringTransaction).filter(
        RecurringTransaction.user_id == user_id,
        RecurringTransaction.active == True,
        RecurringTransaction.next_run_date <= today
    ).all()

    generated = []

    for item in due_items:
        # Create real transaction
        if item.type == "expense":
            new_expense = Expense(
                amount=item.amount,
                description=item.description,
                category_id=item.category_id,
                user_id=user_id
            )
            db.add(new_expense)
            generated.append(new_expense)

        elif item.type == "income":
            new_income = Income(
                amount=item.amount,
                description=item.description,
                category_id=item.category_id,
                user_id=user_id
            )
            db.add(new_income)
            generated.append(new_income)

        # Update next_run_date
        if item.frequency == "weekly":
            item.next_run_date += timedelta(weeks=1)
        elif item.frequency == "monthly":
            item.next_run_date = item.next_run_date.replace(
                month=item.next_run_date.month % 12 + 1
            )
        elif item.frequency == "yearly":
            item.next_run_date = item.next_run_date.replace(
                year=item.next_run_date.year + 1
            )

    db.commit()
    return generated

# Saving Goals CRUD

def create_savings_goal(db: Session, data: schemas.SavingsGoalCreate, user_id: int):
    goal = SavingsGoal(
        name=data.name,
        target_amount=data.target_amount,
        current_amount=data.current_amount,
        deadline=data.deadline,
        user_id=user_id
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal

def get_savings_goals(db: Session, user_id: int):
    return db.query(SavingsGoal).filter(
        SavingsGoal.user_id == user_id
    ).all()

def update_savings_goal(db: Session, goal_id: int, data: schemas.SavingsGoalUpdate):
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id
    ).first()

    if not goal:
        return None

    if data.name is not None:
        goal.name = data.name
    if data.target_amount is not None:
        goal.target_amount = data.target_amount
    if data.current_amount is not None:
        goal.current_amount = data.current_amount
    if data.deadline is not None:
        goal.deadline = data.deadline

    db.commit()
    db.refresh(goal)
    return goal

def delete_savings_goal(db: Session, goal_id: int):
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id
    ).first()

    if not goal:
        return None

    db.delete(goal)
    db.commit()
    return True

def contribute_to_goal(db: Session, goal_id: int, amount: float):
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id
    ).first()

    if not goal:
        return None

    goal.current_amount += amount
    db.commit()
    db.refresh(goal)
    return goal

# Yearly Summary CRUD

from sqlalchemy import extract, func

def get_yearly_summary(db: Session, user_id: int, year: int):
    # Total income
    total_income = db.query(func.sum(Income.amount)).filter(
        Income.user_id == user_id,
        extract('year', Income.created_at) == year
    ).scalar() or 0

    # Total expenses
    total_expenses = db.query(func.sum(Expense.amount)).filter(
        Expense.user_id == user_id,
        extract('year', Expense.created_at) == year
    ).scalar() or 0

    # Category breakdown
    category_breakdown = db.query(
        Category.name,
        func.sum(Expense.amount)
    ).join(Expense, Expense.category_id == Category.id).filter(
        Expense.user_id == user_id,
        extract('year', Expense.created_at) == year
    ).group_by(Category.name).all()

    # Monthly totals (for charts)
    monthly_income = db.query(
        extract('month', Income.created_at).label("month"),
        func.sum(Income.amount)
    ).filter(
        Income.user_id == user_id,
        extract('year', Income.created_at) == year
    ).group_by("month").all()

    monthly_expenses = db.query(
        extract('month', Expense.created_at).label("month"),
        func.sum(Expense.amount)
    ).filter(
        Expense.user_id == user_id,
        extract('year', Expense.created_at) == year
    ).group_by("month").all()

    return {
        "year": year,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net": total_income - total_expenses,
        "category_breakdown": [
            {"category": name, "amount": amount}
            for name, amount in category_breakdown
        ],
        "monthly_income": [
            {"month": int(month), "amount": amount}
            for month, amount in monthly_income
        ],
        "monthly_expenses": [
            {"month": int(month), "amount": amount}
            for month, amount in monthly_expenses
        ]
    }
