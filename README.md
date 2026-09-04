# 💰 Finance App Backend (FastAPI)
**Version:** v1.0.0-backend-complete  
A fully‑featured, production‑ready backend for a personal finance management application.  
Built with **FastAPI**, **SQLAlchemy**, and **JWT authentication**, this backend powers a complete financial tracking system including expenses, incomes, categories, budgets, summaries, recurring transactions, and savings goals.

---

## 🚀 Features

### 🔐 Authentication & Security
- User registration & OAuth2 password bearer login  
- JWT-based authentication  
- Direct `bcrypt` password hashing  
- Scoped database queries providing full multi-user data isolation (IDOR protection)  
- Strict environment-variable validation via `pydantic-settings`

### 💸 Transactions
- Create, update, delete **expenses**  
- Create, update, delete **incomes**  
- Category assignment  
- Filtering & querying  
- Timezone-aware UTC timestamps  

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
- Robust calendar rollover handling variable months and leap years via `python-dateutil`  
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

- **FastAPI** (Python 3.10+)
- **SQLAlchemy ORM**
- **SQLite** (dev) / PostgreSQL-ready
- **Pydantic v2** & **Pydantic-Settings**
- **JWT Authentication** (`python-jose` / `pyjwt`) & **Bcrypt**
- **Testing:** Pytest, HTTPX
- **Server:** Uvicorn

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

```text
app/
│
├── core/
│   ├── config.py          # Environment settings validation
│   ├── core_auth.py       # Authentication dependencies & get_current_user
│   ├── database.py        # Engine, SessionLocal, and declarative Base
│   ├── jwt.py             # Token encoding/decoding utilities
│   └── security.py        # Password hashing via bcrypt
│
├── models.py              # SQLAlchemy database tables & relationships
├── routes/
│   ├── routes_auth.py
│   ├── expenses.py
│   ├── incomes.py
│   ├── categories.py
│   ├── budgets.py
│   ├── summary.py
│   ├── recurring.py
│   └── goals.py
│
├── crud.py                # Isolated, user-scoped database queries
├── schemas.py             # Pydantic v2 request/response models (ConfigDict)
└── main.py                # FastAPI app initialisation & router mounting

tests/
├── conftest.py            # Isolated in-memory SQLite fixtures & TestClient
├── test_auth_and_expenses.py
└── test_recurring.py

Installation & Setup
1. Clone the repository
Bash
git clone [https://github.com/PhillipOyolu/Finance-app-Backend.git](https://github.com/PhillipOyolu/Finance-app-Backend.git)
cd Finance-app-Backend
2. Create a virtual environment
Using standard Python:

Bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
Or using uv:

Bash
uv venv
3. Install dependencies
Bash
pip install -r requirements.txt
(Or with uv: uv sync)

4. Configure Environment Variables
Create a .env file in the root directory (refer to .env.example):

Code snippet
SECRET_KEY=your_super_secret_key_minimum_16_characters
DATABASE_URL=sqlite:///./finance.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
5. Run the server
Bash
uvicorn app.main:app --reload
Server runs at:

http://127.0.0.1:8000

Interactive API documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

🧪 Automated Testing
The backend includes a comprehensive automated test suite testing registration, login, cross-user isolation (IDOR checks), and calendar-dependent recurring transaction algorithms. Tests run against an isolated in-memory SQLite database.

Execute all tests with:
Bash
pytest

📌 API Overview:

Authentication:
POST /auth/signup
POST /auth/login

Expenses:
POST /expenses/
GET /expenses/
PUT /expenses/{id}
DELETE /expenses/{id}

Incomes:
POST /incomes/
GET /incomes/
PUT /incomes/{id}
DELETE /incomes/{id}

Categories:
POST /categories/
GET /categories/

Budgets:
POST /budgets/overall
POST /budgets/category
GET /budgets/

Summaries:
GET /summary/monthly?year=2024&month=5
GET /summary/yearly?year=2024

Recurring Transactions:
POST /recurring/
GET /recurring/
PUT /recurring/{id}
DELETE /recurring/{id}
POST /recurring/run

Savings Goals:
POST /goals/
GET /goals/
PUT /goals/{id}
DELETE /goals/{id}
POST /goals/{id}/contribute?amount=50

🏁 Project Status:
Backend: COMPLETE
This repository represents the final backend version of the Finance App.

All core features are implemented, hardened against IDOR, fully tested with pytest, and ready for frontend integration.

Next Phase: Frontend (React / Next.js)
The upcoming frontend repository will include:

Dashboard UI
Charts (income, expenses, trends)
Budget progress bars
Savings goal visualisation
Recurring transaction management
Authentication UI
Mobile-friendly layout

🏷 GitHub Release Tag
This backend version is officially tagged as: v1.0.1-backend-complete

📬 Contact
Phillip Oyolu
Junior Developer
GitHub: https://github.com/PhillipOyolu
LinkedIn: https://www.linkedin.com/in/phillipoyolu/