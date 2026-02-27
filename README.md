# 🏗 Tenant Payment Platform

A backend system simulating a multi-tenant SaaS onboarding flow with idempotent payment webhook handling.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square)
![Celery](https://img.shields.io/badge/Celery-background%20tasks-37814A?style=flat-square&logo=celery)

---

## 🚀 Project Overview

This project models a real-world SaaS onboarding system where:

1. A tenant signs up
2. A payment is processed via webhook
3. The tenant is activated upon successful payment
4. Duplicate webhooks are handled safely

The system ensures **database-level correctness**, **transaction safety**, and **idempotent webhook handling** — all critical in production systems.

---

## 🧠 Architecture

### Domain Model

```
Tenant (1) ───────── (N) Payment
```

- Each tenant has a unique `order_id`
- Payments reference tenants via `tenant_id`
- Duplicate webhooks are prevented via database constraints

---

## 🗄 Database Schema

### `tenants`

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| email | String | Unique |
| order_id | String | Unique, Not Null |
| status | Enum | `PAYMENT_PENDING` / `ACTIVE` |
| created_at | Timestamp | Default `now()` |

### `payments`

| Column | Type | Constraints |
|---|---|---|
| id | UUID | Primary Key |
| payment_id | String | Unique |
| tenant_id | UUID | FK → `tenants.id` |
| status | Enum | `INITIATED` / `SUCCESS` / `FAILED` |
| created_at | Timestamp | Default `now()` |

---

## 🔥 Idempotent Webhook Handling

Payment providers may:
- Retry webhooks
- Send duplicate events
- Send concurrent events

Instead of relying on in-memory checks, this system uses:
- `UNIQUE(payment_id)` constraint
- `flush()` to trigger DB validation early
- `try/except IntegrityError`
- Explicit `rollback()` on duplicate

### Why This Is Production-Grade

| Risk | Protection |
|---|---|
| Race conditions | DB-level `UNIQUE` constraint |
| Double activation | Conditional status update |
| Duplicate financial entries | `IntegrityError` + rollback |
| Webhook retries | Idempotent response |

---

## 🔁 Payment Flow

### 1️⃣ Tenant Creation
- Generates unique `order_id`
- Status set to `PAYMENT_PENDING`

### 2️⃣ Successful Webhook
- Insert payment record
- Conditionally update tenant status to `ACTIVE`
- Commit transaction

### 3️⃣ Duplicate Webhook
- `UNIQUE` constraint violation detected
- Rollback executed
- Safe response returned — no duplicate row created

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| **FastAPI** | Async web framework |
| **PostgreSQL** | Relational database |
| **SQLAlchemy 2.0** | Async ORM |
| **Alembic** | Database migrations |
| **Celery** | Background task processing |
| **Uvicorn** | ASGI server |

---

## ▶️ Running Locally

### 1. Clone Repository

```bash
git clone https://github.com/your-username/tenant-payment-platform.git
cd tenant-payment-platform
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Database

```bash
createdb tenant_db
```

> Make sure PostgreSQL is running locally.

### 5. Run Migrations

```bash
alembic upgrade head
```

### 6. Start Application

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Manual Testing

### Create Tenant

`POST /tenants/`

```json
{
  "email": "user@example.com"
}
```

### Process Payment Webhook

`POST /payments/webhook`

```json
{
  "payment_id": "pay_1001",
  "tenant_id": "<tenant_id>",
  "status": "SUCCESS"
}
```

### Duplicate Webhook Test

Send the same `payment_id` again.

**Expected behavior:**
- No crash
- No duplicate row inserted
- Response: `duplicate_ignored`

---

## 🧩 Future Enhancements

- [ ] Introduce Order domain (`Tenant → Order → Payment`)
- [ ] Subscription billing support
- [ ] Concurrency stress testing
- [ ] Logging & monitoring integration
- [ ] CI/CD pipeline
- [ ] Production Docker setup
- [ ] Event-driven architecture

---

## 📌 Backend Concepts Demonstrated

- Idempotent API design
- Database-level integrity enforcement
- Transaction management with async SQLAlchemy
- Proper rollback handling
- Race condition mitigation
- Webhook reliability engineering

---

## 👨‍💻 Author

**Shourya Sinha**

---

```bash
git add README.md
git commit -m "docs: add professional README"
git push
```
