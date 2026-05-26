from fastapi import FastAPI
from app.core.database import Base, engine

from app.routes.expenses import router as expenses_router
from app.routes.incomes import router as incomes_router
from app.routes.categories import router as categories_router
from app.routes.summary import router as summary_router
from app.routes.transactions import router as transactions_router
from app.routes.routes_auth import router as auth_router
from app.routes.budgets import router as budgets_router

# Database Initialization
Base.metadata.create_all(bind=engine)

# FastAPI App Instance
app = FastAPI(title="Finance API", version="1.0.0")

# Routers
app.include_router(expenses_router)
app.include_router(incomes_router)
app.include_router(categories_router)
app.include_router(summary_router)
app.include_router(transactions_router)
app.include_router(auth_router)
app.include_router(budgets_router)

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Finance app backend is running!"}

