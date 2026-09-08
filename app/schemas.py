from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


# Expense Schemas
class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Income Schemas
class IncomeBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Category Schemas
class CategoryBase(BaseModel):
    name: str
    type: str  # "income" or "expense"

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Budget Schemas
class BudgetBase(BaseModel):
    amount: float
    month: int
    year: int
    category_id: Optional[int] = None

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Recurring Transaction Schemas
class RecurringTransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None
    type: str  # "income" or "expense"
    frequency: str  # "weekly", "monthly", "yearly"
    next_run_date: date
    active: bool = True

class RecurringTransactionCreate(RecurringTransactionBase):
    pass

class RecurringTransaction(RecurringTransactionBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# Saving Goal Schemas
class SavingsGoalBase(BaseModel):
    name: str
    target_amount: float
    current_amount: float = 0.0
    deadline: Optional[date] = None

class SavingsGoalCreate(SavingsGoalBase):
    pass

class SavingsGoalUpdate(BaseModel):
    name: Optional[str] = None
    target_amount: Optional[float] = None
    current_amount: Optional[float] = None
    deadline: Optional[date] = None

class SavingsGoal(SavingsGoalBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Transaction Schemas
class TransactionBase(BaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    category: Optional[str] = "General"
    type: str  # "income" or "expense"
    date: datetime

    model_config = ConfigDict(from_attributes=True)


# Dashboard Summary Schema
class DashboardSummary(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    recent_transactions: List[TransactionBase]