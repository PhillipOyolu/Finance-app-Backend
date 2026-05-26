from pydantic import BaseModel
from datetime import datetime
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

