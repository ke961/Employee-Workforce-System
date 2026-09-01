# Employee Workforce Management System (EMS)

A state-of-the-art, enterprise-grade, role-based **Employee Workforce Management System (EMS)** designed for remote, hybrid, and on-site teams. Built with a **FastAPI** Python backend and a modern vanilla **JavaScript/CSS3** single-page frontend.

---

## 🌟 Overview & Key Capabilities

The platform provides an end-to-end workforce experience across 13 core enterprise modules, featuring live micro-interactions, dark/light theme switching, universal keyboard shortcuts, and smooth CSS animations.

---

## 🚀 Key Modules & Features

### 1. ⚡ Quick Access & User Experience (UX)
- **One-Click Demo Sign-In Cards**: Sign in instantly as *System Admin*, *Sarah Connor (Designer)*, *Michael Scott (Manager)*, or *Keya Rahman (HR)* without typing credentials.
- **Universal Command Palette (`Ctrl + K` / `Cmd + K`)**: Press `Ctrl + K` anywhere to launch a floating command dialog and jump directly to any section.
- **Interactive Topbar Notification Center**: Bell icon with unread count badge (`3`), live activity feed dropdown (*Expense Approvals*, *New Policies*, *Peer Kudos*), and "Clear All" action.
- **Home Page Motion & Animations**: Animated fluid gradient mesh background, levitating status badges, live ticking digital workstation clock, staggered card entry transitions, and drifting ambient background orbs.

### 2. 👥 Workforce & Directory Management
- **Staff Directory (`/api/employees`)**: Search team members by name/title, filter by department, view phone & email contacts, and click **🔍 Inspect Profile** to open the rich Employee Detail Modal Drawer.
- **Work Shift Roster (`/api/shifts`)**: Manage shift designations (Morning, DevOps On-Call), start/end times, work days, and locations (*Remote Flexible*, *HQ Office*, *Hybrid*).
- **IT Asset Inventory (`/api/assets`)**: Track laptops, 4K monitors, YubiKeys, and mobile test devices with serial numbers, asset tags (`AST-2026-001`), and status (*Assigned*, *Available*, *Maintenance*).

### 3. ⭐ Performance, Culture & Policy
- **Performance & Peer Kudos (`/api/reviews`)**: Interactive 1–5 star rating reviews, manager feedback logs, and a peer recognition shoutout wall.
- **Document Center (`/api/documents`)**: Policy repository cards (*Code of Conduct*, *Security & VPN Policy*, *PTO Policy*) with mandatory acknowledgment tracking.
- **Training & Skills Hub (`/api/trainings`)**: Assign security & compliance courses, monitor completion progress bars, and mark courses as completed.

### 4. 💰 Compensation, Talent & Engagement Hub (New)
- **Salary & Payslips (`/api/payslips`)**: Issue monthly employee payroll with auto calculation of Gross Pay, Allowances, Bonuses, and Deductions (Tax, Insurance, 401k). Features a corporate **Printable Official Payslip Invoice Modal** with 1-click PDF/Print export.
- **Recruitment & ATS Pipeline (`/api/recruitment`)**: Publish job openings, track candidate pipeline across stages (*Applied*, *Screening*, *Interview*, *Offered*, *Hired*, *Rejected*), star ratings, and a **1-Click "Hire & Onboard" action** that automatically provisions an employee profile and onboarding checklist.
- **Workforce Team Messenger (`/api/chat`)**: Real-time collaborative channel spaces (`#general`, `#engineering`, `#hr-helpdesk`, `#watercooler`) with active participant counts, avatars, and fast message stream.
- **Pulse Surveys & Ideas Box (`/api/surveys`)**: Launch interactive company pulse polls with real-time percentage progress bars and an upvotable employee innovation suggestion board with review statuses (*Under Review*, *Planned*, *In Progress*, *Implemented*).

### 5. 📊 Operations, Analytics & Financials
- **Executive Analytics (`/api/analytics`)**: KPI metric cards, expense category breakdown, department headcount allocation visual bar charts, and **1-click CSV Report Exports** (Attendance, Leave, Expenses).
- **Attendance & Workstation Clock**: Real-time clock in / clock out, live shift timers, total work duration calculations, and status badges.
- **Payroll & Expense Claims**: Submit reimbursement requests (AWS Cloud, Figma Org, Client Dinners) with receipt attachments and manager approval status.
- **Team Calendar & Events (`/api/calendar`)**: Event timeline displaying company holidays, all-hands townhalls, hackathons, and workshops with date badges.

---

## 📂 Project Structure

```text
Employee-Workforce-System/
├── backend/
│   ├── app.py                # FastAPI main server & database seeding logic
│   ├── auth.py               # JWT authentication & password hashing (Passlib/Bcrypt)
│   ├── database.py           # SQLAlchemy SQLite engine setup
│   ├── models.py             # SQLAlchemy ORM database models (21 models)
│   ├── schemas.py            # Pydantic request & response validation schemas
│   ├── requirements.txt      # Python dependencies
│   └── routers/
│       ├── analytics.py      # Executive analytics & CSV report export endpoints
│       ├── announcements.py  # Company broadcasts router
│       ├── assets.py         # IT hardware inventory router
│       ├── attendance.py     # Workstation clock in/out & attendance history router
│       ├── calendar.py       # Team calendar & events router
│       ├── chat.py           # Team messenger & channels router
│       ├── dashboard.py      # Aggregated dashboard metrics router
│       ├── documents.py      # Policy document center & acknowledgment router
│       ├── employees.py      # Staff directory CRUD router
│       ├── expenses.py       # Expense reimbursement claims router
│       ├── leave.py          # Leave request router
│       ├── login.py          # Authentication & JWT tokens router
│       ├── okrs.py           # Objectives & Key Results router
│       ├── onboarding.py     # Onboarding task checklist router
│       ├── payslips.py       # Salary & payslip compensation router
│       ├── recruitment.py    # Job postings & ATS candidate pipeline router
│       ├── reviews.py        # Performance reviews & peer kudos router
│       ├── shifts.py         # Work shift roster router
│       ├── surveys.py        # Pulse surveys & innovation ideas router
│       ├── tasks.py          # Kanban project task router
│       └── trainings.py      # Training & skills certification router
├── frontend/
│   ├── index.html            # Main single-page application view & modals
│   ├── login.html            # Standalone login template
│   ├── dashboard.html        # Standalone dashboard view
│   ├── css/
│   │   ├── styles.css        # Comprehensive design system, dark mode & animations
│   │   └── login.css         # Sign-in page layout styling
│   └── js/
│       └── script.js         # Single-page application logic, API client & event listeners
├── walkthrough.md            # Detailed feature & test walkthrough
├── implementation_plan.md    # Architecture implementation plan
└── README.md                 # Project documentation
```

---

## 🔑 Authentication & Pre-configured Accounts

You can sign in using **One-Click Demo Sign-In** on the login page or enter any of the credentials below:

| Role | Name | Email | Password | Department |
| :--- | :--- | :--- | :--- | :--- |
| **System Admin** | System Administrator | `admin@gmail.com` | `Admin123` | Administration |
| **UX Designer** | Sarah Connor | `employee@gmail.com` | `Employee123` | Product |
| **Manager** | Michael Scott | `manager@gmail.com` | `Manager123` | Operations |
| **HR Head** | Keya Rahman | `hr@gmail.com` | `HR123!` | People Operations |
| **Lead Engineer** | Alex Rivera | `alex.rivera@ems.local` | `Employee123!` | Engineering |
| **DevOps Lead** | David Chen | `david.chen@ems.local` | `Employee123!` | Engineering |
| **Product Manager**| Emma Watson | `emma.watson@ems.local` | `Employee123!` | Product |
| **Support Lead** | James Wilson | `james.wilson@ems.local` | `Employee123!` | Support |
| **Finance Controller**| Sophia Martinez | `sophia.martinez@ems.local` | `Employee123!` | Finance |
| **Backend Engineer**| Daniel Kim | `daniel.kim@ems.local` | `Employee123!` | Engineering |
| **Growth Marketer**| Olivia Taylor | `olivia.taylor@ems.local` | `Employee123!` | Marketing |

---

## 🛠️ Installation & Local Setup

### 1. Start the Backend API Server (FastAPI)

```powershell
# Navigate to the backend directory
cd backend

# Create & activate a virtual environment (optional)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install backend dependencies
pip install -r requirements.txt

# Start the FastAPI uvicorn server
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

- **Backend API URL**: `http://127.0.0.1:8000`
- **Interactive Swagger API Docs**: `http://127.0.0.1:8000/docs`

---

### 2. Start the Frontend Single-Page App

Open `frontend/index.html` directly in any modern web browser or serve via a local static server:

```powershell
# Open index.html directly or serve using Python http.server
cd frontend
python -m http.server 5173
```

- **Frontend App URL**: `http://127.0.0.1:5173` or open `frontend/index.html` directly in browser.

---

## 🔬 API Endpoint Summary

| Module | Base Path | Methods |
| :--- | :--- | :--- |
| **Auth** | `/api/auth` | `POST /login`, `GET /me`, `PATCH /me` |
| **Staff Directory** | `/api/employees` | `GET /`, `POST /`, `DELETE /{id}` |
| **Work Shifts** | `/api/shifts` | `GET /`, `POST /`, `DELETE /{id}` |
| **IT Assets** | `/api/assets` | `GET /`, `POST /`, `PATCH /{id}`, `DELETE /{id}` |
| **Calendar Events**| `/api/calendar/events` | `GET /`, `POST /`, `DELETE /{id}` |
| **Trainings** | `/api/trainings` | `GET /`, `POST /`, `PATCH /{id}/status`, `DELETE /{id}` |
| **Salary & Payslips** | `/api/payslips` | `GET /`, `POST /`, `GET /{id}`, `PATCH /{id}/status`, `DELETE /{id}` |
| **Recruitment & ATS** | `/api/recruitment` | `GET /jobs`, `POST /jobs`, `DELETE /jobs/{id}`, `GET /candidates`, `POST /candidates`, `PATCH /candidates/{id}/stage`, `POST /candidates/{id}/convert-to-employee`, `DELETE /candidates/{id}` |
| **Team Messenger** | `/api/chat` | `GET /channels`, `GET /messages`, `POST /messages` |
| **Surveys & Ideas** | `/api/surveys` | `GET /`, `POST /`, `POST /{id}/vote`, `GET /ideas`, `POST /ideas`, `POST /ideas/{id}/upvote`, `PATCH /ideas/{id}/status`, `DELETE /ideas/{id}` |
| **Performance** | `/api/reviews` | `GET /performance`, `POST /performance`, `GET /kudos`, `POST /kudos` |
| **Documents** | `/api/documents` | `GET /`, `POST /`, `POST /{id}/acknowledge` |
| **Analytics** | `/api/analytics` | `GET /metrics`, `GET /export/attendance`, `GET /export/leave`, `GET /export/expenses` |

---

## 🎨 Design System & Technologies

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, SQLite, Pydantic, Passlib, PyJWT, Uvicorn
- **Frontend**: HTML5, Vanilla JavaScript (ES6+), Vanilla CSS3 Design System with CSS Custom Properties
- **Aesthetics**: Glassmorphic cards, mesh ambient glow animations, dark/light theme tokens, responsive layouts

---

## 📄 License

This project is licensed under the **[MIT License](file:///c:/Users/Hp/Desktop/Employee-Workforce-System/LICENSE)**. Free to use, modify, and distribute for personal or commercial applications.

<!-- Pair badge update for ke961 -->
