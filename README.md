<div align="center">

# 🏥 MediCare HMS

### *A full-stack web application for managing hospital operations — patients, doctors, appointments, and treatments.*

[![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

<img src="https://img.shields.io/badge/Status-Complete-success" alt="Status">
<img src="https://img.shields.io/badge/Course-App%20Dev%20II-brightgreen" alt="App Dev II">
<img src="https://img.shields.io/badge/IIT%20Madras-Data%20Science-blue" alt="IIT Madras">

---

### 👨‍🎓 Student: Shrishti Gupta | Roll: 23f2004336 | Email: 23f2004336@ds.study.iitm.ac.in

</div>

<br/>

> **Note:** This project features role-based access control (Admin, Doctor, Patient) and automated background jobs managed by Celery and Redis.

## 🚀 Setup & Installation

> [!WARNING]  
> You need **5 terminals running simultaneously**. Keep them all open throughout development.

**Prerequisites:** Python 3.8+, Node.js 14+, Redis Server, npm 6+

### Terminal 1 — Redis Server
```bash
# Start Redis — must be running before anything else
redis-server

# Verify it works (should return PONG)
redis-cli ping
