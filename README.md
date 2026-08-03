# EMS Project — Separate HTML, CSS, JavaScript and Python Files

## Folder structure

```text
EMS_Separated_Files/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── backend/
│   ├── app.py
│   └── requirements.txt
└── README.md
```

## Run the project

Open PowerShell inside the `backend` folder:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Demo accounts

Employee:
- Email: employee@ems.local
- Password: Employee123!

Manager:
- Email: manager@ems.local
- Password: Manager123!

Admin:
- Email: admin@ems.local
- Password: Admin123!

The frontend files are fully separate:
- `frontend/index.html`
- `frontend/styles.css`
- `frontend/app.js`

The Python backend is:
- `backend/app.py`
