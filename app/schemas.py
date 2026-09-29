from datetime import date, datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, ConfigDict


# --- Base Configuration Model ---
class AppBaseModel(BaseModel):
    """
    Base model for all schemas:
    - use_enum_values=True: Unwraps Enums to raw strings ('expense') on dump/access.
    - from_attributes=True: Enables reading directly from SQLAlchemy ORM instances.
    """
    model_config = ConfigDict(
        use_enum_values=True,
        from_attributes=True
    )


# --- Base Case-Insensitive Enum ---
class CaseInsensitiveEnum(str, Enum):
    """
    Normalizes any input string to lowercase and strips surrounding whitespace.
    Allows 'INCOME', 'Income', ' income ', and 'InCoMe' to match gracefully.
    """
    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            val_clean = value.strip().lower()
            for member in cls:
                if member.value == val_clean:
                    return member
        return None


# --- Domain Enumerations ---
class TransactionTypeEnum(CaseInsensitiveEnum):
    INCOME = "income"
    EXPENSE = "expense"


class FrequencyEnum(CaseInsensitiveEnum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


# --- Expense Schemas ---
class ExpenseBase(AppBaseModel):
    amount: float = Field(gt=0, description="Amount must be strictly positive")
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = Field(None, description="Nullable category reference")


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(AppBaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None


class Expense(ExpenseBase):
    id: int
    user_id: int
    created_at: datetime


# --- Income Schemas ---
class IncomeBase(AppBaseModel):
    amount: float = Field(gt=0, description="Amount must be strictly positive")
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = Field(None, description="Nullable category reference")


class IncomeCreate(IncomeBase):
    pass


class IncomeUpdate(AppBaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None


class Income(IncomeBase):
    id: int
    user_id: int
    created_at: datetime


# --- Category Schemas ---
class CategoryBase(AppBaseModel):
    name: str = Field(min_length=1, max_length=50, description="Category name cannot be empty")
    type: TransactionTypeEnum


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime


# --- Budget Schemas ---
class BudgetBase(AppBaseModel):
    amount: float = Field(ge=0, description="Budget cannot be negative")
    month: int = Field(ge=1, le=12, description="Month must be between 1 and 12")
    year: int = Field(ge=2020, le=2100, description="Year must be within a realistic calendar range")
    category_id: Optional[int] = Field(None, description="Nullable for overall budget")


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: int
    user_id: int
    created_at: datetime


# --- Recurring Transaction Schemas ---
class RecurringTransactionBase(AppBaseModel):
    amount: float = Field(gt=0, description="Recurring amount must be positive")
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    type: TransactionTypeEnum
    frequency: FrequencyEnum
    next_run_date: date
    active: bool = True


class RecurringTransactionCreate(RecurringTransactionBase):
    pass


class RecurringTransactionUpdate(AppBaseModel):
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = None
    type: Optional[TransactionTypeEnum] = None
    frequency: Optional[FrequencyEnum] = None
    next_run_date: Optional[date] = None
    active: Optional[bool] = None


class RecurringTransaction(RecurringTransactionBase):
    id: int
    user_id: int
    created_at: datetime


# --- Savings Goal Schemas ---
class SavingsGoalBase(AppBaseModel):
    name: str = Field(min_length=1, max_length=100)
    target_amount: float = Field(gt=0, description="Target must be positive")
    current_amount: float = Field(ge=0, default=0.0)
    deadline: Optional[date] = None


class SavingsGoalCreate(SavingsGoalBase):
    pass


class SavingsGoalUpdate(AppBaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    target_amount: Optional[float] = Field(None, gt=0)
    current_amount: Optional[float] = Field(None, ge=0)
    deadline: Optional[date] = None


class SavingsGoal(SavingsGoalBase):
    id: int
    user_id: int
    created_at: datetime


# --- User & Auth Schemas ---
class UserBase(AppBaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8, description="Passwords must be at least 8 characters")


class User(UserBase):
    id: int


# --- Unified Read Models ---
class TransactionRead(AppBaseModel):
    id: int
    amount: float
    description: Optional[str] = None
    category_name: str
    type: TransactionTypeEnum
    date: datetime


class DashboardSummary(AppBaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    recent_transactions: List[TransactionRead]