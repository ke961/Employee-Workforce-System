# Employee Workforce Management System (EMS)

[![Live App on Render](https://img.shields.io/badge/Render-Live%20App-46e3b7?logo=render&logoColor=white)](https://employee-workforce-system-1.onrender.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

A state-of-the-art, enterprise-grade, role-based **Employee Workforce Management System (EMS)** designed for remote, hybrid, and on-site teams. Built with a high-performance **Python FastAPI** backend and a modern, responsive **Vanilla JavaScript & CSS3** Single-Page Application (SPA) frontend.

---

## 🌐 Live Deployments

| Platform | Role | URL | Status |
| :--- | :--- | :--- | :--- |
| **Render** | **Full-Stack (Frontend + Backend)** | [https://employee-workforce-system-1.onrender.com/](https://employee-workforce-system-1.onrender.com/) | ✅ Active |
| **API Docs** | **Interactive Swagger UI** | [https://employee-workforce-system-1.onrender.com/docs](https://employee-workforce-system-1.onrender.com/docs) | ✅ Active |

---

## 🌟 Key Capabilities & Enterprise Modules

The platform provides a complete workforce experience across 16 core modules:

### 1. ⚡ Quick Access & Modern UX
- **One-Click Demo Sign-In Cards**: Instant access as *System Admin*, *Sarah Connor (Designer)*, *Michael Scott (Manager)*, or *Keya Rahman (HR)* with zero typing.
- **Universal Command Palette (`Ctrl + K` / `Cmd + K`)**: Quick-jump search dialog to instantly navigate to any module or execute actions.
- **Notification Center**: Real-time activity bell with badge counters for approvals, kudos, and policy updates.
- **Glassmorphic Motion Design**: Ambient animated SVG mesh grid, smooth gradient shifts, ripple button interactions, and card entrance reveals.

### 2. 🕒 Attendance & Workstation
- **Live Digital Clock & Shift Station**: Real-time ticking clock with animated status chips.
- **Circular Progress Ring**: SVG shift progress ring tracking workday duration.
- **One-Click Clock In / Clock Out**: Live work session logging with milestone confetti celebrations.
- **Attendance History Log**: Detailed shift records with automatic duration calculations.

### 3. 👥 Workforce & Directory Management
- **Staff Directory (`/api/employees`)**: Searchable employee cards, department filters, and an interactive **Inspect Profile** modal drawer.
- **Work Shift Roster (`/api/shifts`)**: Manage shifts (Morning, DevOps On-Call), start/end times, and work locations (*Remote*, *HQ Office*, *Hybrid*).
- **IT Asset Inventory (`/api/assets`)**: Hardware tracking (MacBooks, 4K Displays, YubiKeys) with serial numbers, asset tags, and assignment statuses.

### 4. ⭐ Performance, Culture & Policy
- **Performance Reviews & Kudos (`/api/reviews`)**: 1–5 star interactive reviews, manager feedback logs, and a peer recognition shoutout wall.
- **Document Center (`/api/documents`)**: Corporate policy repository (*Code of Conduct*, *Security Guidelines*) with digital acknowledgment tracking.
- **Training & Certifications (`/api/trainings`)**: Security and compliance training tracking with visual progress indicators.

### 5. 💰 Compensation, Talent & Engagement
- **Salary & Payslips (`/api/payslips`)**: Monthly payroll generation with auto calculations (Gross, Allowances, Deductions) and a printable official payslip invoice.
- **Recruitment & ATS Pipeline (`/api/recruitment`)**: Job openings, applicant stages (*Applied*, *Screening*, *Interview*, *Offered*, *Hired*), and a **1-Click "Hire & Onboard"** action.
- **Workforce Messenger (`/api/chat`)**: Multi-channel team chat (`#general`, `#engineering`, `#hr-helpdesk`, `#watercooler`).
- **Pulse Polls & Ideas Box (`/api/surveys`)**: Real-time company polls and upvotable employee innovation suggestions.

### 6. 📊 Operations, Leave & Expenses
- **Leave Management (`/api/leave`)**: Submit, track, and approve annual, sick, and emergency leaves with real-time balance calculations.
- **Payroll & Expense Claims (`/api/expenses`)**: Submit reimbursement requests with merchant details, category tags, and approval tracking.
- **OKRs & Goals (`/api/okrs`)**: Objectives and Key Results with nested progress tracking.
- **Tasks & Kanban (`/api/tasks`)**: Priority-ranked task boards (*To Do*, *In Progress*, *In Review*, *Done*).
- **Executive Analytics (`/api/analytics`)**: Visual KPI metric cards, department headcount charts, and **1-Click CSV Exports** (Attendance, Leave, Expenses).

---

## 🔑 Demo Login Accounts

Test the platform instantly with any of the pre-seeded accounts:

| Role | Name | Email | Password | Department |
| :--- | :--- | :--- | :--- | :--- |
| **System Admin** | System Administrator | `admin@gmail.com` | `Admin123` | Administration |
| **UX Designer** | Sarah Connor | `employee@gmail.com` | `Employee123` | Product |
| **Operations Manager** | Michael Scott | `manager@gmail.com` | `Manager123` | Operations |
| **Head of HR** | Keya Rahman | `hr@gmail.com` | `HR123!` | People Operations |
| **Lead Engineer** | Alex Rivera | `alex.rivera@ems.local` | `Employee123!` | Engineering |
| **DevOps Lead** | David Chen | `david.chen@ems.local` | `Employee123!` | Infrastructure |
| **Product Manager**| Emma Watson | `emma.watson@ems.local` | `Employee123!` | Product |

---

## 🚀 Deployment Guide

### Render Deployment (Full-Stack Unified)

The project includes an Infrastructure-as-Code [render.yaml](render.yaml) specification:

1. Push code to your GitHub repository.
2. Go to **[dashboard.render.com](https://dashboard.render.com)** → **New +** → **Blueprint**.
3. Select your repository. Render will automatically read `render.yaml`.
4. Click **Apply**. Render will install dependencies, seed the database, and launch both backend and frontend on a single URL.

```yaml
# Build & Start commands executed by Render:
buildCommand: pip install -r backend/requirements.txt
startCommand: cd backend && gunicorn app:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

---

## 🛠️ Local Development Setup

### 1. Backend Server (FastAPI)

```bash
# Navigate to backend
cd backend

# Create & activate a virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server with live reload
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

- **Backend API**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/api/health`

### 2. Frontend Development

```bash
# Navigate to frontend
cd frontend

# Run local dev server (Vite)
npm install
npm run dev
```

- **Frontend Dev URL**: `http://127.0.0.1:5173`

---

## 📂 Project Architecture

```text
Employee-Workforce-System/
├── backend/
│   ├── app.py                # Main FastAPI entry point & static frontend mount
│   ├── auth.py               # JWT authentication & password hashing
│   ├── database.py           # SQLAlchemy database engine (SQLite / PostgreSQL)
│   ├── models.py             # 21 SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic validation schemas
│   ├── requirements.txt      # Python dependencies
│   └── routers/              # 16 modular API routers
│       ├── analytics.py      # Executive reporting & CSV exports
│       ├── announcements.py  # Company announcement broadcasts
│       ├── assets.py         # IT hardware inventory
│       ├── attendance.py     # Clock in/out & shift history
│       ├── calendar.py       # Team calendar events
│       ├── chat.py           # Team channels & messaging
│       ├── dashboard.py      # Summary metrics aggregation
│       ├── documents.py      # Company policies & acknowledgments
│       ├── employees.py      # Staff directory management
│       ├── expenses.py       # Expense reimbursements
│       ├── leave.py          # Leave requests & balances
│       ├── login.py          # Auth & token management
│       ├── okrs.py           # Objectives & Key Results
│       ├── onboarding.py     # Onboarding task checklist
│       ├── payslips.py       # Salary & payslip compensation
│       ├── recruitment.py    # Job postings & ATS pipeline
│       ├── reviews.py        # Performance & peer kudos
│       ├── shifts.py         # Shift schedule rosters
│       ├── surveys.py        # Pulse polls & suggestion box
│       ├── tasks.py          # Task & Kanban boards
│       └── trainings.py      # Training courses & skills
├── frontend/
│   ├── index.html            # Main unified SPA markup
│   ├── css/
│   │   └── styles.css        # Design tokens, themes & animations
│   ├── js/
│   │   └── script.js         # Single-page application logic & API client
│   └── vite.config.mjs       # Vite build setup with asset copy plugin
├── render.yaml               # Render Infrastructure-as-Code blueprint
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 🎨 Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite / PostgreSQL, Pydantic, Passlib, PyJWT, Gunicorn, Uvicorn
- **Frontend**: Vanilla HTML5, Vanilla JavaScript (ES6+), Modern CSS3 with Custom Properties & Glassmorphism
- **Design System**: Dark/Light mode theme system, responsive CSS Grid / Flexbox layouts, accessible keyboard shortcuts
- **Deployment**: Render (Python Web Service with direct static frontend serving)

---

## 📄 License

This project is open-sourced under the **[MIT License](LICENSE)**.
