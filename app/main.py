from fastapi import FastAPI
from app.core.database import Base, engine

from app.routes import expenses
from app.routes import incomes
from app.routes import categories
from app.routes import summary
from app.routes import transactions
from app.routes import routes_auth
from app.routes import budgets
from app.routes import recurring
from app.routes import goals

# Database Initialization
Base.metadata.create_all(bind=engine)

# FastAPI App Instance
app = FastAPI(title="Finance API", version="1.0.0")

# Routers
app.include_router(expenses.router)
app.include_router(incomes.router)
app.include_router(categories.router)
app.include_router(summary.router)
app.include_router(transactions.router)
app.include_router(routes_auth.router)
app.include_router(budgets.router)
app.include_router(recurring.router)
app.include_router(goals.router)

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Finance app backend is running!"}

