<div align="center">

# 🏥 MediCare Hospital Management System 💊

### *Streamlining Healthcare Operations: A Comprehensive Full-Stack Solution for Doctors, Patients, and Administrators*

[![Flask](https://img.shields.io/badge/Flask-3.1+-black.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-4FC08D.svg?logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-07405E.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Redis](https://img.shields.io/badge/Redis-7.0+-DC382D.svg?logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-5.0+-37814A.svg?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-7952B3.svg?logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

<img src="https://img.shields.io/badge/Status-Complete-success" alt="Status">
<img src="https://img.shields.io/badge/Course-App%20Dev%20II-brightgreen" alt="App Dev II">
<img src="https://img.shields.io/badge/IIT%20Madras-Data%20Science-blue" alt="IIT Madras">

---

### 🌟 A robust, role-based web application leveraging asynchronous background jobs and a decoupled architecture to manage hospital workflows seamlessly.

[🚀 Quick Start](#-getting-started) • [👥 Features & Roles](#-features--roles) • [🔗 API Details](#-api-endpoints) • [🗄️ Database](#-database-design) • [👥 Author](#-about-the-author)

</div>

---

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🔧 Technical Implementation](#-technical-implementation)
- [👥 Features & Roles](#-features--roles)
- [🛠️ Technologies Used](#️-technologies-used)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
- [🔗 API Endpoints](#-api-endpoints)
- [⏰ Background Jobs](#-background-jobs)
- [🗄️ Database Design](#-database-design)
- [👥 About the Author](#-about-the-author)
- [📞 Connect With Me](#-connect-with-me)

---

## 🎯 Project Overview

<div align="center">

### 💡 **The Challenge**

*How can we efficiently digitize hospital operations while ensuring secure access control, preventing scheduling conflicts, and automating routine administrative tasks?*

</div>

This project addresses the operational bottlenecks in healthcare facilities by providing a unified digital platform. By integrating a Flask RESTful API with a reactive Vue.js frontend and Celery-powered background workers, the system automates appointment reminders, monthly reporting, and secure patient data management.

### 🎲 System Entities

A highly normalized database handles the complex relationships between the core hospital entities.

<table align="center">
<tr>
<td align="center"><b>🧑‍⚕️ Patients</b></td>
<td align="center"><b>🩺 Doctors</b></td>
<td align="center"><b>📅 Appointments</b></td>
<td align="center"><b>💊 Treatments</b></td>
</tr>
<tr>
<td align="center">Self-registering users</td>
<td align="center">Specialized medical staff</td>
<td align="center">Conflict-free bookings</td>
<td align="center">Complete medical records</td>
</tr>
</table>

---

## ✨ Key Features

### 🔍 Advanced System Capabilities

<table>
<tr>
<td width="50%">

#### 🔐 **Security & Access**
- 🛡️ JWT-based authentication
- 👤 Role-based access control (RBAC)
- 🔒 Secure password hashing
- 🚫 Protected API endpoints

</td>
<td width="50%">

#### ⚡ **Performance & Automation**
- 🔴 Redis caching for fast data retrieval
- 🌿 Celery Beat for scheduled tasks
- 📥 Asynchronous CSV exports
- 📧 Automated HTML email reports

</td>
</tr>
</table>

---

## 🏗️ System Architecture

<div align="center">

### 🎯 **Decoupled Client-Server Architecture**

<img src="https://img.shields.io/badge/Frontend-Vue.js-4FC08D?style=for-the-badge" alt="Frontend">
<img src="https://img.shields.io/badge/Backend-Flask-black?style=for-the-badge" alt="Backend">
<img src="https://img.shields.io/badge/Workers-Celery-37814A?style=for-the-badge" alt="Workers">

</div>

### 🌟 Component Interaction

<div align="center">

┌─────────────────────────────────────────────────────────────┐│                    🏥 System Components                     │├─────────────────────────────────────────────────────────────┤│                                                             ││  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       ││  │    Vue.js    │  │  Flask API   │  │   SQLite DB  │       ││  │  📱 Client   │──▶  ⚙️ Server   │──▶  🗄️ Storage  │       ││  └──────────────┘  └───────┬──────┘  └──────────────┘       ││                            │                                ││                            ▼                                ││  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       ││  │ Celery Beat  │  │ Redis Broker │  │ Celery Worker│       ││  │ ⏰ Scheduler │──▶  🔴 Cache    │◀──  🏭 Executor │       ││  └──────────────┘  └──────────────┘  └───────┬──────┘       ││                                              │              ││                                              ▼              ││                                      ┌──────────────┐       ││                                      │  Async Tasks │       ││                                      │ 📧 Emails/CSV│       ││                                      └──────────────┘       │└─────────────────────────────────────────────────────────────┘
</div>

---

## 👥 Features & Roles

### 👑 Admin (Pre-created)
*Dashboard with real-time stats, full system control.*
* Add, update, and delete doctor profiles with specialties.
* View all hospital appointments globally.
* Remove/blacklist patients with automated cascade deletion.
* Manually trigger Celery background jobs (Reminders/Reports).

### 🩺 Doctor (Managed by Admin)
*Dedicated portal for medical professionals.*
* Set dynamic 7-day availability schedules.
* Confirm or cancel pending patient appointments.
* Create and edit detailed treatment records (diagnosis, prescription).
* View complete medical histories of assigned patients.

### 🧑‍⚕️ Patient (Self-Registration)
*End-user booking and history portal.*
* Search doctors by name or department specialization.
* Book conflict-free appointments based on real-time availability.
* Reschedule or cancel existing bookings.
* **Export complete medical history as a CSV (Async Background Job).**

---

## 🛠️ Technologies Used

<div align="center">

### 🐍 Backend Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)

### 💚 Frontend Stack

[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)](https://vuejs.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com/)

### ⚙️ DevOps & Background Workers

[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)

</div>

---

## 📁 Project Structure

```text
📦 Hospital_Management_System
┣ 📂 backend                 # Flask Application API
┃ ┣ 📄 app.py               # Routes, Setup, Celery Tasks
┃ ┣ 📄 models.py            # SQLAlchemy Schema (6 Tables)
┃ ┣ 📄 config.py            # Configurations & JWT Secrets
┃ ┣ 📂 templates
┃ ┃ ┗ 📄 monthly_report.html# Jinja2 Email Template
┃ ┣ 📂 static/uploads       # Async CSV Exports
┃ ┗ 🗄️ hospital.db          # Auto-generated database
┣ 📂 frontend                # Vue.js SPA
┃ ┣ 📂 src
┃ ┃ ┣ 📂 views
┃ ┃ ┃ ┣ 📄 AdminDashboard.vue
┃ ┃ ┃ ┣ 📄 DoctorDashboard.vue
┃ ┃ ┃ ┗ 📄 PatientDashboard.vue
┃ ┃ ┗ 📂 router
┃ ┃   ┗ 📄 index.js         # Vue Router Configuration
┃ ┣ 📄 package.json
┃ ┗ 📄 vue.config.js
┣ 📄 requirements.txt
┗ 📄 README.md
🚀 Getting Started📋 Prerequisites[!WARNING]You need 5 terminals running simultaneously. Keep them all open throughout development.💻 5-Terminal Setup Guide🔴 Terminal 1: Redis ServerBash# Start the message broker
redis-server

# Verify connection
redis-cli ping
🐍 Terminal 2: Flask BackendBashcd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
💚 Terminal 5: Vue FrontendBashcd frontend
npm install
npm run serve
# Runs on http://localhost:8080
🌿 Terminal 3: Celery WorkerBashcd backend
source venv/bin/activate
celery -A app.celery worker --loglevel=info
# Executes background tasks
⏰ Terminal 4: Celery BeatBashcd backend
source venv/bin/activate
celery -A app.celery beat --loglevel=info
# Schedules recurring jobs
🔑 Default Admin LoginPlaintextEmail: admin@hospital.com
Pass:  admin123
🔗 API Endpoints🔓 Public RoutesEndpointMethodDescriptionCache/registerPOSTPatient self-registration-/loginPOSTAuthenticate & get JWT-/doctorsGETList doctors & availability🟢 60s Redis👑 Admin Routes (JWT Required)EndpointMethodDescription/admin/dashboardGETSystem statistics/admin/add_doctorPOSTCreate doctor profile/admin/doctor/<id>DELETECascade delete doctor/admin/trigger/dailyPOSTManual trigger: reminders🩺 Doctor Routes (JWT Required)EndpointMethodDescription/doctor/appointmentsGETView assigned appointments/doctor/schedulePUTUpdate 7-day availability/doctor/treat_patientPOSTCreate medical record🧑‍⚕️ Patient Routes (JWT Required)EndpointMethodDescription/patient/bookPOSTConflict-free booking/patient/my_appointmentsGETView history & treatments/patient/export_historyPOSTTrigger async CSV export (Returns 202)⏰ Background Jobs⚙️ Celery Task Configuration🔔 Daily Patient RemindersPythonSchedule: crontab(hour=8, minute=0)
Type: Beat Scheduled Task
Runs at 8:00 AM IST. Queries all appointments for the current day and sends personalized email reminders to patients.📊 Monthly Doctor ReportsPythonSchedule: crontab(day='1', hour=0)
Type: Beat Scheduled Task
Runs on the 1st of every month. Compiles completed treatments and sends a styled HTML email report to doctors.📥 Patient CSV ExportPythonTrigger: User Requested via UI
Type: Async Worker Task
User clicks "Export" -> HTTP 202 returned immediately -> Worker generates CSV -> Saves to static/uploads/ -> Emails download link.🗄️ Database Design🎯 Entity Relationship & Cascade RulesMaster TableChild TableRelationshipCascade ActionUsersPatientsOne-to-Oneall, deleteUsersDoctorsOne-to-Oneall, deletePatientsAppointmentsOne-to-Manyall, delete-orphanDoctorsAppointmentsOne-to-Manyall, delete-orphanAppointmentsTreatmentsOne-to-Oneall, delete-orphanDepartmentsDoctorsOne-to-ManySET NULL👥 About the Author👩‍💻 Shrishti GuptaPassionate Data Science Student | Full Stack Developer | Problem Solver🎓 Academic BackgroundBachelor of Science in Data Science & Applications 🏛️ Indian Institute of Technology Madras (IIT Madras)🎓 Roll No: 23f2004336📚 Currently pursuing dual diplomas in:🤖 Diploma in Data Science (DL GENAI Track)💻 Diploma in Programming🌟 Areas of Interest🌐 Full-Stack Development  •  🤖 Machine Learning  •  🧠 Deep Learning / GenAI
🔬 API Architecture  •  📈 Predictive Analytics  •  🎯 Automation
💡 Problem Solving  •  🗄️ Database Design  •  🔍 Research
📞 Connect With Me🤝 Let's Collaborate and Build Something Amazing!💼 LinkedIn💻 GitHub📧 Email📊 GitHub Stats💖 Thank you for visiting!Made with ❤️ by Shrishti Gupta | IIT Madras Data Science StudentLast Updated: January 2026
