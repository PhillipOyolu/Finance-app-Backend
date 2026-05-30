from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True

# Category Schemas

class CategoryBase(BaseModel):
    name: str
    type: str  # "income" or "expense"

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True

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

    class Config:
        from_attributes = True

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

    class Config:
        from_attributes = True
