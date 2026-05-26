# ShopStack — React + FastAPI + mysql

A full-stack product management app where:
- **Anyone** (no login) can browse all products
- **Logged-in owners** can create, edit, and delete **only their own** products

---

## Project Structure

```
project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── index.css
│   │
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       │
│       ├── context/
│       │   └── AuthContext.jsx
│       │
│       ├── components/
│       │   ├── Navbar.jsx
│       │   ├── ProductCard.jsx
│       │   └── ProductModal.jsx
│       │
│       └── pages/
│           ├── ProductsPage.jsx
│           ├── DashboardPage.jsx
│           ├── LoginPage.jsx
│           └── RegisterPage.jsx
│
└── docker-compose.yml
```


---
## Installation
---

### Clone Repository

```bash
git clone <repo-url>
cd product-management-system
````

---

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on:

```
http://localhost:5173
```

---

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

Run server:

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```
http://localhost:8000
```

---

## MySQL Setup

Create database:

```sql
CREATE DATABASE shopstack;
```

Environment variable:

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/shopstack
```

---

## Docker (Optional)

```bash
docker compose up --build
```

---

## Features

* User authentication (JWT)
* Product CRUD operations
* Dashboard management
* REST API backend
* Responsive frontend

---

## API Documentation

Swagger UI:

```
http://localhost:8000/docs
```
---

## Run Project

Run backend and frontend separately or use Docker Compose.

```
```


<img width="1874" height="948" alt="image" src="https://github.com/user-attachments/assets/8ee377e6-a5a5-4f64-a853-22567aedb3ca" />

<img width="1919" height="972" alt="image" src="https://github.com/user-attachments/assets/658b1eef-c796-442c-bf5f-e74fc7ed115d" />
