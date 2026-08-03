# Employee Workforce Management System (EMS)

A comprehensive, role-based Employee Workforce Management prototype designed for remote and hybrid teams. Features attendance tracking, leave management, onboarding checklists, OKR progress tracking, and user profile management.

---

## Project Structure

```text
Employee-Workforce-System/
├── frontend/
│   ├── index.html        # Main application layout (Login & Dashboard)
│   ├── login.html        # Standalone login page
│   ├── dashboard.html    # Standalone dashboard template
│   ├── css/
│   │   ├── styles.css    # Unified application stylesheet
│   │   ├── login.css     # Login page styling
│   │   └── style.css     # General utility styling
│   ├── js/
│   │   ├── script.js     # Main dashboard application logic
│   │   └── login.js      # Form validation & auth helpers
│   ├── vite.config.js    # Frontend dev server config
│   └── package.json
├── backend/
│   ├── app.py            # FastAPI main application server & router setup
│   ├── auth.py           # JWT authentication & password hashing logic
│   ├── models.py         # SQLAlchemy database models
│   ├── schemas.py        # Pydantic request/response schemas
│   ├── database.py      # Database engine configuration
│   └── requirements.txt  # Python backend dependencies
└── README.md
```

---

## Running the Project

### 1. Start the Backend Server (FastAPI)

Open a terminal inside the `backend` folder:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The backend API server will run at:
- **API URL**: `http://127.0.0.1:8000`
- **Swagger Documentation**: `http://127.0.0.1:8000/docs`

---

### 2. Start the Frontend Server

Open a terminal inside the `frontend` folder:

```powershell
cd frontend
npm install
npm run dev
```

The frontend application will run at:
- **App URL**: `http://127.0.0.1:5173`

---

## Authentication & User Credentials

The sign-in interface is a single, clean input form. Enter any of the registered role-specific credentials below to sign in directly to your personalized workspace dashboard:

| Role | Email | Password |
| :--- | :--- | :--- |
| **System Admin** | `admin@gmail.com` | `Admin123` |
| **System Admin (Local)** | `admin@ems.local` | `Admin123!` |
| **Employee** | `employee@gmail.com` | `Employee123` |
| **Employee (Local)** | `employee@ems.local` | `Employee123!` |
| **Manager** | `manager@gmail.com` | `Manager123` |
| **Manager (Local)** | `manager@ems.local` | `Manager123!` |
| **HR Operations** | `hr@gmail.com` | `HR123!` |

---

## Key Features

- **Direct Role-Based Direct Login**: Sign in using specific credentials for Admin, Manager, Employee, or HR.
- **Attendance Tracking**: Real-time clock in / clock out and total work duration logging.
- **Leave Request System**: Submit annual, sick, or casual leave applications and monitor status.
- **Onboarding Checklist**: Track onboarding tasks and completion progress.
- **OKR Tracker**: Set objectives, key results, and monitor target percentages.
- **Profile Management**: Update full name, email, job title, department, and phone details.
