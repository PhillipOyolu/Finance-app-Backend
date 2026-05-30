# 💰 Finance App Backend (FastAPI)
**Version:** v1.0.0-backend-complete  
A fully‑featured, production‑ready backend for a personal finance management application.  
Built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**, this backend powers a complete financial tracking system including expenses, incomes, categories, budgets, summaries, recurring transactions, and savings goals.

---

## 🚀 Features

### 🔐 Authentication
- User registration & login  
- JWT-based authentication  
- Secure password hashing  
- Full multi-user data isolation  

### 💸 Transactions
- Create, update, delete **expenses**  
- Create, update, delete **incomes**  
- Category assignment  
- Filtering & querying  
- Automatic timestamps  

### 🗂 Categories
- Custom categories per user  
- Category-based analytics  
- Integrated into summaries & budgets  

### 📊 Summaries & Analytics
- **Monthly summary**  
  - Total income  
  - Total expenses  
  - Net  
  - Category breakdown  
- **Yearly summary**  
  - Yearly totals  
  - Monthly trend data  
  - Category breakdown  

### 💼 Budgets
- Overall monthly budget  
- Category-specific budgets  
- Budget performance tracking  
- Integrated into summaries  

### 🔁 Recurring Transactions
- Weekly, monthly, yearly recurring items  
- Auto-generation of real transactions  
- Supports both incomes & expenses  
- Pause/resume recurring items  
- Manual trigger endpoint for development  

### 🎯 Savings Goals
- Create savings goals  
- Track progress  
- Optional deadlines  
- Contribute to goals  
- Integrated into future dashboard analytics  

---

## 🧱 Tech Stack

- **FastAPI** (Python)
- **SQLAlchemy ORM**
- **SQLite** (dev) / PostgreSQL-ready
- **Pydantic v2**
- **JWT Authentication**
- **Uvicorn**

---

## 🧰 Development Tools

This project was developed using **uv**, a modern Python package and environment manager.

While not required to run the backend, `uv` provides:

- extremely fast dependency installation  
- automatic virtual environment handling  
- reproducible builds  
- a cleaner workflow than pip + venv  

If you prefer, you can still install dependencies using standard `pip` commands — the backend works either way.

---

## 📁 Project Structure

app/
│
├── core/
│   ├── auth.py
│   ├── database.py
│   └── security.py
│
├── models/
│   ├── user.py
│   ├── expense.py
│   ├── income.py
│   ├── category.py
│   ├── budget.py
│   ├── recurring_transaction.py
│   └── savings_goal.py
│
├── routes/
│   ├── auth.py
│   ├── expenses.py
│   ├── incomes.py
│   ├── categories.py
│   ├── budgets.py
│   ├── summary.py
│   ├── transactions.py
│   ├── recurring.py
│   └── goals.py
│
├── crud.py
├── schemas.py
└── main.py

---

## ▶️ Running the Project

uv venv
uv sync
uv run fastapi dev app/main.py

---

## 🛠 Installation & Setup

### 1. Clone the repository

https://github.com/PhillipOyolu/Finance-app-Backend


### 2. Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run the server

uvicorn app.main:app --reload

Server runs at:  
**http://127.0.0.1:8000**

Interactive API docs:  
**http://127.0.0.1:8000/docs**

---

## 📌 API Overview

### Authentication
- `POST /auth/register`
- `POST /auth/login`

### Expenses
- `POST /expenses/`
- `GET /expenses/`
- `PUT /expenses/{id}`
- `DELETE /expenses/{id}`

### Incomes
- `POST /incomes/`
- `GET /incomes/`
- `PUT /incomes/{id}`
- `DELETE /incomes/{id}`

### Categories
- `POST /categories/`
- `GET /categories/`

### Budgets
- `POST /budgets/overall`
- `POST /budgets/category`
- `GET /budgets/`

### Summaries
- `GET /summary/monthly?year=2024&month=5`
- `GET /summary/yearly?year=2024`

### Recurring Transactions
- `POST /recurring/`
- `GET /recurring/`
- `PUT /recurring/{id}`
- `DELETE /recurring/{id}`
- `POST /recurring/run`

### Savings Goals
- `POST /goals/`
- `GET /goals/`
- `PUT /goals/{id}`
- `DELETE /goals/{id}`
- `POST /goals/{id}/contribute?amount=50`

---

## 🏁 Project Status

### **Backend: COMPLETE**  
This repository represents the **final backend version** of the Finance App.

All core features are implemented, tested, and ready for frontend integration.

### **Next Phase: Frontend (React / Next.js)**  
The next repository will include:

- Dashboard UI  
- Charts (income, expenses, trends)  
- Budget progress bars  
- Savings goal visualisation  
- Recurring transaction management  
- Authentication UI  
- Mobile-friendly layout 

---

## 🧰 Development Tools

This project was developed using **uv**, a modern Python package and environment manager.

While not required to run the backend, `uv` provides:

- extremely fast dependency installation  
- automatic virtual environment handling  
- reproducible builds  
- a cleaner workflow than pip + venv  

If you prefer, you can still install dependencies using standard `pip` commands — the backend works either way.

---

## 🏷 GitHub Release Tag

This backend version is officially tagged as: v1.0.0-backend-complete


## 📬 Contact

**Phillip Oyolu**  
Junior Developer  
GitHub: https://github.com/PhillipOyolu
LinkedIn: https://www.linkedin.com/in/phillipoyolu/