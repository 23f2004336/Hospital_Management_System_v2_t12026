<div align="center">

<img src="https://img.icons8.com/fluency/96/hospital.png" alt="MediCare HMS" width="80"/>

# 🏥 MediCare — Hospital Management System

**A production-grade, full-stack web application for digitizing hospital operations**  
*Role-based · Async-first · Conflict-safe · Cache-optimized*

[![Flask](https://img.shields.io/badge/Flask-3.1+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Celery](https://img.shields.io/badge/Celery-5.0+-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![IIT Madras](https://img.shields.io/badge/IIT%20Madras-BS%20Data%20Science-blue?style=flat-square)](https://study.iitm.ac.in/)
[![App Dev II](https://img.shields.io/badge/Course-App%20Development%20II-orange?style=flat-square)](#)
[![Stack](https://img.shields.io/badge/Stack-Flask%20%2B%20Vue.js%20%2B%20Celery-informational?style=flat-square)](#)

</div>

---

## 📌 Overview

**MediCare** is a role-based hospital management web application that solves real operational pain points in healthcare — scheduling conflicts, paper records, and disconnected workflows. It delivers a **decoupled REST API** (Flask) paired with a **reactive SPA** (Vue.js 3), powered by **asynchronous task workers** (Celery + Redis) that automate appointment reminders, doctor reports, and patient data exports.

> **What makes this technically interesting:** Beyond standard CRUD, this system implements JWT-based RBAC across three distinct roles, database-level double-booking prevention, Redis response caching with TTL, and three Celery job patterns — time-scheduled, periodic monthly, and user-triggered async with HTTP 202 Accepted.

---

## 🧠 System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                          CLIENT                              │
│          Vue.js 3 SPA  ·  Vue Router  ·  Axios  ·  Bootstrap │
└────────────────────────┬─────────────────────────────────────┘
                         │  REST API  (JWT Bearer Token)
┌────────────────────────▼─────────────────────────────────────┐
│                      FLASK BACKEND                           │
│     RESTful Routes  ·  Flask-SQLAlchemy ORM  ·  JWT Auth     │
│     Flask-Caching  ·  Flask-Mail  ·  Jinja2 Email Templates  │
└───────────┬──────────────────────────────┬───────────────────┘
            │                              │
┌───────────▼──────────┐     ┌─────────────▼──────────────────┐
│      SQLite DB       │     │      Redis (Broker + Cache)    │
│  6 normalized tables │     │  TTL caching · Task queue      │
└──────────────────────┘     └─────────────┬──────────────────┘
                                           │
                              ┌────────────▼───────────────────┐
                              │      Celery Worker + Beat      │
                              │  • Daily reminders (8 AM IST)  │
                              │  • Monthly HTML reports (1st)  │
                              │  • Async CSV export on-demand  │
                              └────────────────────────────────┘
```

### Engineering Decisions

| Concern | Approach | Rationale |
|---|---|---|
| Authentication | JWT via `Flask-JWT-Extended` | Stateless; roles encoded in token payload |
| Double-booking | DB constraint + API validation layer | Prevents race conditions at the data level |
| API performance | `Flask-Caching` + Redis TTL | High-read endpoints (doctor list) served from cache |
| Heavy exports | Celery async task → HTTP 202 | Non-blocking UX; user notified by email on completion |
| DB initialization | `db.create_all()` + programmatic seed | No manual DB creation; admin seeded automatically |
| Password security | `Werkzeug generate_password_hash` | Passwords never stored as plain text |

---

## 👥 Roles & Features

### 👑 Admin
> Pre-seeded on first run — no registration endpoint. Single superuser identified by `role = 'admin'`.

- Dashboard with live counts: total doctors, patients, appointments
- Add, update, and delete doctor profiles (name, specialization, qualification, fee, contact)
- View and manage **all** appointments across the hospital
- Search patients by name, email, or contact information
- Remove or blacklist doctors and patients (cascades to related records)
- **Manually trigger** daily reminder and monthly report Celery jobs from the dashboard

### 🩺 Doctor
> Accounts created by Admin only. Doctors cannot self-register.

- Private dashboard: upcoming (Booked/Confirmed) and past (Completed/Cancelled) appointments
- Set a custom **7-day availability schedule** — start time, end time, off-duty days
- Confirm or cancel patient appointments
- Fill treatment form: diagnosis, prescription, notes, next visit date → marks appointment Completed
- View and edit full medical history of any assigned patient

### 🧑‍⚕️ Patient
> Full self-service portal — register, search, book, manage.

- Self-registration and login with hashed passwords
- Search doctors by name or specialization (dropdown filter)
- View doctor availability for the next 7 days before booking
- Book appointments with **conflict prevention** — same doctor, date, and time cannot be double-booked
- Reschedule or cancel existing bookings
- View appointment history: status, diagnosis, prescription, notes, next visit date
- Edit personal profile: name, gender, date of birth, address, phone
- **Trigger async CSV export** of full treatment history — download link delivered by email

---

## ⚙️ Background Jobs (Celery + Redis)

Three production-grade Celery patterns implemented:

### 🔔 Daily Patient Reminders — Scheduled (Celery Beat)
```
Trigger : Automated · Every day at 08:00 AM IST
Pattern : crontab(hour=8, minute=0)
```
Queries all appointments with today's date → sends a personalized email reminder to each patient via Flask-Mail.

---

### 📊 Monthly Doctor Activity Report — Periodic (Celery Beat)
```
Trigger : Automated · 1st of every month at 00:00
Pattern : crontab(day_of_month=1, hour=0)
```
Compiles all completed appointments and treatments for the prior month → renders a **styled Jinja2 HTML email** → delivered to each doctor's registered inbox.

---

### 📥 Patient CSV Export — User-Triggered Async (Celery Worker)
```
Trigger : Patient clicks "Export" in dashboard
Response: HTTP 202 Accepted (immediate, non-blocking)
```
Celery worker generates a CSV containing:
`user_id · username · consulting_doctor · appointment_date · diagnosis · treatment · next_visit`

File saved to `static/uploads/` → download link emailed to patient on completion.

---

## 🗄️ Database Schema

Six normalized tables with explicit cascade rules — created entirely via `SQLAlchemy` models, no manual DB setup.

```
┌─────────────────────────────────────────────────────────────────────┐
│  USERS           DEPARTMENTS                                        │
│  ─────────────   ────────────────                                   │
│  id (PK)         department_id (PK)                                 │
│  username        department_name                                    │
│  password        description                                        │
│  email               │                                              │
│  role                │ contains (1:M)                               │
│  is_active           ▼                                              │
│  first_name    DOCTORS ────────────────────────────────┐            │
│  last_name     ─────────────────────────────────────   │            │
│      │         id (PK)   user_id (FK→Users)            │            │
│      │         department_id (FK→Departments, SET NULL) │            │
│      │         specialization   experience             │            │
│      │         qualification    consultation_fee       │            │
│      │         availability     address   phone_number │            │
│      │                                    attends (1:M)│            │
│  has profile (1:1)                                     │            │
│      │                        APPOINTMENTS ◄───────────┘            │
│      ▼                        ─────────────────────────             │
│  PATIENTS                     id (PK)                               │
│  ─────────────────────        patient_id (FK→Patients, cascade)     │
│  id (PK)                      doctor_id  (FK→Doctors,  cascade)     │
│  user_id (FK→Users)           appointment_date   appointment_time   │
│  date_of_birth                appointment_status  reason            │
│  gender  address                      │                             │
│  phone_number                         │ results in (1:1)            │
│      │ books (1:M)                    ▼                             │
│      └─────────────────►  TREATMENTS                                │
│                           ──────────────────────────────────        │
│                           id (PK)   appointment_id (FK, cascade)    │
│                           diagnosis     prescription                │
│                           notes         treatment_date              │
│                           next_visit                                │
└─────────────────────────────────────────────────────────────────────┘
```

**Cascade policy:**
- Delete `Doctor` → cascades to their `Appointments` → cascades to `Treatments`
- Delete `Patient` → cascades to their `Appointments` → cascades to `Treatments`
- Delete `Department` → sets `doctor.department_id = NULL` (non-destructive)

---

## 🔗 API Endpoints

### 🔓 Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register` | Patient self-registration |
| `POST` | `/login` | Authenticate (all roles) → returns JWT |
| `GET` | `/doctors` | Public doctor list with availability ✅ *Redis cached* |

### 👑 Admin *(JWT Required)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin/stats` | Dashboard: total doctors, patients, appointments |
| `GET` | `/admin/doctors` | List all doctors |
| `POST` | `/admin/doctors` | Add new doctor profile |
| `PUT` | `/admin/update_doctor/<id>` | Update doctor details |
| `GET` | `/admin/patients` | List all patients |
| `DELETE` | `/admin/patient/<id>` | Remove / blacklist patient |
| `PUT` | `/admin/patient/<id>` | Edit patient record |
| `GET` | `/admin/appointments` | View all hospital appointments |
| `POST` | `/admin/trigger/daily` | Manually fire daily reminder job |
| `POST` | `/admin/trigger/monthly` | Manually fire monthly report job |

### 🩺 Doctor *(JWT Required)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/doctor/appointments` | View own appointments |
| `GET/PUT` | `/doctor/schedule` | Get or update 7-day availability |
| `PUT` | `/doctor/appointment/<id>` | Mark Confirmed or Cancelled |
| `POST` | `/doctor/treat_patient` | Save diagnosis, prescription, notes |
| `GET` | `/doctor/patient_history/<id>` | Full patient treatment history |
| `PUT` | `/doctor/update_treatment/<id>` | Edit an existing treatment record |

### 🧑‍⚕️ Patient *(JWT Required)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/patient/doctors` | Doctor list with availability |
| `GET` | `/patient/my_appointments` | Appointment history + treatment details |
| `POST` | `/patient/book` | Book appointment (conflict-checked) |
| `PUT` | `/patient/appointment/<id>/cancel` | Cancel a booking |
| `PUT` | `/patient/appointment/<id>/reschedule` | Reschedule a booking |
| `GET/PUT` | `/patient/profile` | View or update personal profile |
| `POST` | `/patient/export_history` | Trigger async CSV export → returns **202** |

---

## 🛠️ Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Frontend** | Vue.js 3 | Reactive SPA, component-based UI |
| **HTTP Client** | Axios | API calls from Vue to Flask |
| **Routing** | Vue Router 4 | Client-side routing + JWT route guards |
| **Styling** | Bootstrap 5 | Responsive layout, modals, forms, tables |
| **Backend** | Flask 3.1+ | RESTful API server |
| **ORM** | Flask-SQLAlchemy | Python model definitions, query layer |
| **Auth** | Flask-JWT-Extended | JWT issuance, verification, RBAC |
| **Password Security** | Werkzeug | `generate_password_hash` — no plain-text storage |
| **Database** | SQLite | Normalized 6-table schema, programmatic init |
| **Cache** | Flask-Caching + Redis | TTL-based API response caching |
| **Task Queue** | Celery | Scheduled + async background workers |
| **Broker** | Redis | Celery message broker |
| **Email** | Flask-Mail | Appointment reminders, reports, CSV links |
| **Templates** | Jinja2 | Styled HTML email generation |

---

## 📁 Project Structure

```
Hospital_Management_System/
│
├── backend/
│   ├── app.py                    # Flask app, all routes, Celery task definitions
│   ├── models.py                 # SQLAlchemy models: Users, Patients, Doctors,
│   │                             #   Departments, Appointments, Treatments
│   ├── config.py                 # JWT secret, Redis URL, mail config, cache settings
│   ├── templates/
│   │   └── monthly_report.html   # Jinja2 HTML template for doctor email reports
│   ├── static/
│   │   └── uploads/              # Generated CSV files land here (async export)
│   └── hospital.db               # Auto-created + seeded on first run
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── AdminDashboard.vue
│   │   │   ├── DoctorDashboard.vue
│   │   │   ├── PatientDashboard.vue
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── components/             # Reusable Vue components
│   │   └── router/
│   │       └── index.js            # Route definitions + JWT-based route guards
│   ├── vue.config.js               # Dev proxy → Flask :5000
│   └── package.json
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- Redis running locally (`redis-server`)

### Setup

**1. Clone the repo**
```bash
git clone https://github.com/23f2004336/Hospital_Management_System_v2_t12026.git
cd Hospital_Management_System_v2_t12026/Hospital_Management_System_23f2004336
```

**2. Configure environment**

Create a `.env` file inside `backend/`:
```env
SECRET_KEY=your-flask-secret
JWT_SECRET_KEY=your-jwt-secret
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
REDIS_URL=redis://localhost:6379/0
```

**3. Start all five services** (separate terminals)

```bash
# Terminal 1 — Redis
redis-server

# Terminal 2 — Flask backend (auto-creates DB + seeds admin on first run)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py                          # → http://localhost:5000

# Terminal 3 — Celery worker
cd backend && source venv/bin/activate
celery -A app.celery worker --loglevel=info

# Terminal 4 — Celery beat scheduler
cd backend && source venv/bin/activate
celery -A app.celery beat --loglevel=info

# Terminal 5 — Vue.js frontend
cd frontend && npm install
npm run serve                          # → http://localhost:8080
```

### Default Admin Login
```
Username : admin
Password : admin123
```
> Admin is seeded programmatically — no `/admin/register` endpoint exists by design.

---

## 🔐 Security

- **Password hashing** — Werkzeug's `generate_password_hash`; plain-text passwords are never stored
- **JWT authentication** — tokens issued on login, verified on every protected route
- **Role-based access control** — patients cannot reach admin or doctor routes; enforced at the API layer
- **Ownership enforcement** — doctors can only edit treatment records tied to their own appointments

---

## 🎬 Demo

📽️ **Video Walkthrough:** [Watch on Google Drive](https://drive.google.com/file/d/1gj1xI3O2vo4OZGbRU5oOdfH0OK_6oxd/view?usp=sharing)

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

## 👩‍💻 About the Author

**Shrishti Gupta**  
*Data Science Student · ML Engineer · Full-Stack Developer*

🎓 **B.Sc. Data Science & Applications** — Indian Institute of Technology Madras  
*Dual Diploma: Data Science (Deep Learning & GenAI) + Programming*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shrishti-gupta-iitm/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/23f2004336)

*Open to opportunities in ML Engineering, Backend Development, and Full-Stack roles.*

---

*Made with ❤️ · IIT Madras · Jan 2026*

</div>
