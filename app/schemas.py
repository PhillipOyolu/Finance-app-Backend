from pydantic import BaseModel
from datetime import datetime

# Expense Schemas

class ExpenseBase(BaseModel):
    name: str
    amount: float
    category: str
    category_id: int | None = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Income Schemas

class IncomeBase(BaseModel):
    name: str
    amount: float
    category: str
    category_id: int | None = None

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
