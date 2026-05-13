# Finance-app-Backend
# Personal Finance Tracker (Backend)
A FastAPI backend for tracking income and expenses with full CRUD functionality, database persistence, and clean modular architecture. This project is part of a larger full‑stack personal finance application that will eventually include analytics, summaries, budgeting tools, and a React frontend.

---

## 🚀 Features

### ✔ Income & Expense Tracking
- Create, read, update, and delete income entries  
- Create, read, update, and delete expense entries  
- Automatic timestamps for all transactions  

### ✔ Clean Architecture
- **FastAPI** for API routing  
- **SQLAlchemy** ORM models  
- **Pydantic** schemas for validation  
- **SQLite** database for persistence  
- Modular structure (`models`, `schemas`, `crud`, `main`)  

### ✔ API Documentation
FastAPI automatically generates interactive docs:

- Swagger UI → `http://127.0.0.1:8000/docs`
- ReDoc → `http://127.0.0.1:8000/redoc`

---

## 🗂 Project Structure


---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **SQLite**
- **Uvicorn**

---

## 📌 Endpoints Overview

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/expenses/` | Create a new expense |
| GET    | `/expenses/` | Get all expenses |
| PUT    | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |

### Income
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/incomes/` | Create a new income entry |
| GET    | `/incomes/` | Get all income entries |
| PUT    | `/incomes/{id}` | Update an income entry |
| DELETE | `/incomes/{id}` | Delete an income entry |

---

## ▶️ Running the Project

### 1. Install dependencies

### 2. Start the server

### 3. Open the API docs
Visit:

---

## 📈 Future Enhancements

This backend will continue to evolve. Planned features include:

- Monthly summaries (income vs expenses)
- Category breakdowns
- Budgeting system
- Savings goals
- Recurring transactions
- Authentication (JWT)
- React frontend integration
- Deployment to cloud hosting

---

## 🎯 Purpose of This Project

This project is part of my journey to becoming a full‑stack developer.  
It demonstrates:

- backend engineering skills  
- clean code structure  
- database modelling  
- API design  
- real‑world CRUD operations  

More features will be added as I continue developing the full application.

---

## 📬 Contact

**Phillip Oyolu**  
Junior Developer  
GitHub: https://github.com/PhillipOyolu
LinkedIn: https://www.linkedin.com/in/phillipoyolu/

