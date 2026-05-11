from pydantic import BaseModel
from datetime import datetime

class ExpenseBase(BaseModel):
    name: str
    amount: float
    category: str

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class IncomeBase(BaseModel):
    name: str
    amount: float
    category: str

class IncomeCreate(IncomeBase):
    pass

class Income(IncomeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
