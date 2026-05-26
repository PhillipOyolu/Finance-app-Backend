# Finance Tracker API

A fully featured, secure, multi‑user finance tracking backend built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**.  
This project supports expense tracking, income tracking, category management, budgets, monthly summaries, and transaction filtering.

---

## 🚀 Features

### 🔐 Authentication & Security
- JWT‑based login and signup
- Password hashing with industry‑standard algorithms
- All routes protected and scoped to the authenticated user
- Strict ownership checks on all CRUD operations

### 💸 Expenses & Incomes
- Create, update, delete, and list transactions
- Category assignment
- Automatic timestamping
- Full user isolation

### 🗂 Categories
- Global category system (income + expense types)
- Create, list, and delete categories

### 📊 Monthly Summary
- Total income and expenses
- Net balance
- Category breakdowns
- Percentage distributions
- Raw entries for frontend dashboards

### 🎯 Budgets
- Monthly budgets (overall or category‑specific)
- Budget vs actual spending
- Remaining amount and percentage used
- Integrated directly into the summary endpoint

### 🔎 Transaction Filtering
- Filter by date range, category, amount, or type
- Combined and sorted results

---

## 🛠 Tech Stack

- **FastAPI** (Python)
- **SQLAlchemy ORM**
- **SQLite** (dev) — easily swappable for Postgres
- **uv** for dependency and environment management
- **JWT** for authentication

---

## 📁 Project Structure

app/
├── core/          # auth, security, database
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── crud/          # database operations
├── routes/        # API endpoints
└── main.py        # FastAPI entrypoint

---

## ▶️ Running the Project

uv venv
uv sync
uv run fastapi dev app/main.py

---

## 📌 Roadmap

- Recurring transactions
- Savings goals
- Yearly summaries
- Dashboard endpoint
- Frontend (React or Next.js)

---

## 📄 License

MIT License


---

## 📬 Contact

**Phillip Oyolu**  
Junior Developer  
GitHub: https://github.com/PhillipOyolu
LinkedIn: https://www.linkedin.com/in/phillipoyolu/