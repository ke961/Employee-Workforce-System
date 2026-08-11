# from __future__ import annotations

# import os
# import sqlite3
# from datetime import datetime, timedelta, timezone
# from functools import wraps
# from typing import Any

# import jwt
# from flask import Flask, g, jsonify, request, send_from_directory
# from werkzeug.security import check_password_hash, generate_password_hash


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
# FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
# DB_PATH = os.path.join(BASE_DIR, "ems.db")
# SECRET_KEY = os.environ.get("EMS_SECRET_KEY", "change-this-secret-before-production")

# app = Flask(__name__)
# app.config["JSON_SORT_KEYS"] = False


# # ---------------------------------------------------------------------------
# # Database helpers
# # ---------------------------------------------------------------------------

# def utc_now() -> str:
#     return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# def get_db() -> sqlite3.Connection:
#     if "db" not in g:
#         g.db = sqlite3.connect(DB_PATH)
#         g.db.row_factory = sqlite3.Row
#         g.db.execute("PRAGMA foreign_keys = ON")
#     return g.db


# @app.teardown_appcontext
# def close_db(_error: Exception | None = None) -> None:
#     db = g.pop("db", None)
#     if db is not None:
#         db.close()


# def init_db() -> None:
#     db = sqlite3.connect(DB_PATH)
#     db.execute("PRAGMA foreign_keys = ON")
#     db.executescript(
#         """
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NOT NULL,
#             email TEXT NOT NULL UNIQUE,
#             password_hash TEXT NOT NULL,
#             role TEXT NOT NULL CHECK(role IN ('admin', 'manager', 'employee')),
#             job_title TEXT NOT NULL DEFAULT '',
#             department TEXT NOT NULL DEFAULT '',
#             manager_id INTEGER,
#             leave_balance INTEGER NOT NULL DEFAULT 20,
#             created_at TEXT NOT NULL,
#             FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE SET NULL
#         );

#         CREATE TABLE IF NOT EXISTS attendance (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             clock_in TEXT NOT NULL,
#             clock_out TEXT,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#         );

#         CREATE TABLE IF NOT EXISTS leave_requests (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             leave_type TEXT NOT NULL,
#             start_date TEXT NOT NULL,
#             end_date TEXT NOT NULL,
#             reason TEXT NOT NULL,
#             status TEXT NOT NULL CHECK(status IN ('pending', 'approved', 'denied')),
#             reviewer_id INTEGER,
#             reviewer_note TEXT NOT NULL DEFAULT '',
#             created_at TEXT NOT NULL,
#             updated_at TEXT NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
#             FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE SET NULL
#         );

#         CREATE TABLE IF NOT EXISTS onboarding_tasks (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             title TEXT NOT NULL,
#             completed INTEGER NOT NULL DEFAULT 0,
#             completed_at TEXT,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#         );

#         CREATE TABLE IF NOT EXISTS okrs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             objective TEXT NOT NULL,
#             key_result TEXT NOT NULL,
#             progress INTEGER NOT NULL DEFAULT 0 CHECK(progress BETWEEN 0 AND 100),
#             quarter TEXT NOT NULL,
#             created_at TEXT NOT NULL,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#         );

#         CREATE TABLE IF NOT EXISTS audit_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             actor_id INTEGER,
#             action TEXT NOT NULL,
#             entity_type TEXT NOT NULL,
#             entity_id INTEGER,
#             details TEXT NOT NULL DEFAULT '',
#             created_at TEXT NOT NULL,
#             FOREIGN KEY (actor_id) REFERENCES users(id) ON DELETE SET NULL
#         );
#         """
#     )

#     count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
#     if count == 0:
#         now = utc_now()
#         users = [
#             ("Keya", "admin@ems.local", generate_password_hash("Admin123!"),
#              "admin", "HR Administrator", "People Operations", None, 20, now),
#             ("Hasan Karim", "manager@ems.local", generate_password_hash("Manager123!"),
#              "manager", "Engineering Manager", "Engineering", None, 20, now),
#             ("Shafin", "employee@ems.local", generate_password_hash("Employee123!"),
#              "employee", "Frontend Developer", "Engineering", 2, 18, now),
#             ("Rafi Ahmed", "rafi@ems.local", generate_password_hash("Employee123!"),
#              "employee", "Backend Developer", "Engineering", 2, 16, now),
#         ]
#         db.executemany(
#             """
#             INSERT INTO users
#             (name, email, password_hash, role, job_title, department, manager_id, leave_balance, created_at)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             users,
#         )

#         tasks = [
#             (3, "Complete employee profile", 1, now),
#             (3, "Read remote-work policy", 1, now),
#             (3, "Set up development environment", 0, None),
#             (3, "Meet the engineering manager", 0, None),
#             (4, "Complete employee profile", 1, now),
#             (4, "Read remote-work policy", 0, None),
#             (4, "Set up development environment", 0, None),
#         ]
#         db.executemany(
#             "INSERT INTO onboarding_tasks (user_id, title, completed, completed_at) VALUES (?, ?, ?, ?)",
#             tasks,
#         )

#         db.execute(
#             """
#             INSERT INTO okrs (user_id, objective, key_result, progress, quarter, created_at)
#             VALUES (?, ?, ?, ?, ?, ?)
#             """,
#             (3, "Improve dashboard experience", "Reduce average task completion time by 20%", 45, "Q3 2026", now),
#         )

#         db.execute(
#             """
#             INSERT INTO leave_requests
#             (user_id, leave_type, start_date, end_date, reason, status, created_at, updated_at)
#             VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
#             """,
#             (4, "Annual Leave", "2026-08-10", "2026-08-12", "Family programme", now, now),
#         )
#     db.commit()
#     db.close()


# # ---------------------------------------------------------------------------
# # Authentication and authorization
# # ---------------------------------------------------------------------------

# def create_token(user: sqlite3.Row) -> str:
#     payload = {
#         "sub": str(user["id"]),
#         "role": user["role"],
#         "exp": datetime.now(timezone.utc) + timedelta(hours=8),
#         "iat": datetime.now(timezone.utc),
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# def token_required(view):
#     @wraps(view)
#     def wrapped(*args, **kwargs):
#         auth_header = request.headers.get("Authorization", "")
#         if not auth_header.startswith("Bearer "):
#             return jsonify({"error": "Authentication token is required."}), 401

#         token = auth_header.split(" ", 1)[1]
#         try:
#             payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#             user = get_db().execute(
#                 "SELECT id, name, email, role, job_title, department, manager_id, leave_balance FROM users WHERE id = ?",
#                 (int(payload["sub"]),),
#             ).fetchone()
#             if not user:
#                 raise jwt.InvalidTokenError()
#             g.current_user = user
#         except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError, KeyError):
#             return jsonify({"error": "Invalid or expired token."}), 401

#         return view(*args, **kwargs)
#     return wrapped


# def roles_required(*allowed_roles: str):
#     def decorator(view):
#         @wraps(view)
#         @token_required
#         def wrapped(*args, **kwargs):
#             if g.current_user["role"] not in allowed_roles:
#                 return jsonify({"error": "You do not have permission for this action."}), 403
#             return view(*args, **kwargs)
#         return wrapped
#     return decorator


# def audit(action: str, entity_type: str, entity_id: int | None, details: str = "") -> None:
#     actor_id = g.current_user["id"] if hasattr(g, "current_user") else None
#     get_db().execute(
#         """
#         INSERT INTO audit_logs (actor_id, action, entity_type, entity_id, details, created_at)
#         VALUES (?, ?, ?, ?, ?, ?)
#         """,
#         (actor_id, action, entity_type, entity_id, details, utc_now()),
#     )


# def user_can_review(target_user_id: int) -> bool:
#     current = g.current_user
#     if current["role"] == "admin":
#         return True
#     if current["role"] == "manager":
#         direct_report = get_db().execute(
#             "SELECT id FROM users WHERE id = ? AND manager_id = ?",
#             (target_user_id, current["id"]),
#         ).fetchone()
#         return bool(direct_report)
#     return False


# # ---------------------------------------------------------------------------
# # Frontend route
# # ---------------------------------------------------------------------------

# @app.get("/")
# def index():
#     return send_from_directory(FRONTEND_DIR, "index.html")


# @app.get("/styles.css")
# def styles():
#     return send_from_directory(FRONTEND_DIR, "styles.css")


# @app.get("/app.js")
# def javascript():
#     return send_from_directory(FRONTEND_DIR, "app.js")


# # ---------------------------------------------------------------------------
# # API routes
# # ---------------------------------------------------------------------------

# @app.post("/api/login")
# def login():
#     data = request.get_json(silent=True) or {}
#     email = str(data.get("email", "")).strip().lower()
#     password = str(data.get("password", ""))

#     user = get_db().execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
#     if not user or not check_password_hash(user["password_hash"], password):
#         return jsonify({"error": "Incorrect email or password."}), 401

#     return jsonify(
#         {
#             "token": create_token(user),
#             "user": {
#                 "id": user["id"],
#                 "name": user["name"],
#                 "email": user["email"],
#                 "role": user["role"],
#                 "job_title": user["job_title"],
#             },
#         }
#     )


# @app.get("/api/me")
# @token_required
# def me():
#     user = dict(g.current_user)
#     manager = None
#     if user["manager_id"]:
#         manager_row = get_db().execute(
#             "SELECT id, name, email FROM users WHERE id = ?", (user["manager_id"],)
#         ).fetchone()
#         manager = dict(manager_row) if manager_row else None
#     user["manager"] = manager
#     return jsonify(user)


# @app.get("/api/dashboard")
# @token_required
# def dashboard():
#     db = get_db()
#     user = g.current_user

#     open_attendance = db.execute(
#         "SELECT * FROM attendance WHERE user_id = ? AND clock_out IS NULL ORDER BY id DESC LIMIT 1",
#         (user["id"],),
#     ).fetchone()

#     own_pending = db.execute(
#         "SELECT COUNT(*) FROM leave_requests WHERE user_id = ? AND status = 'pending'",
#         (user["id"],),
#     ).fetchone()[0]

#     tasks_total = db.execute(
#         "SELECT COUNT(*) FROM onboarding_tasks WHERE user_id = ?", (user["id"],)
#     ).fetchone()[0]
#     tasks_done = db.execute(
#         "SELECT COUNT(*) FROM onboarding_tasks WHERE user_id = ? AND completed = 1", (user["id"],)
#     ).fetchone()[0]

#     team_pending = 0
#     employee_count = 0
#     if user["role"] == "manager":
#         team_pending = db.execute(
#             """
#             SELECT COUNT(*)
#             FROM leave_requests lr
#             JOIN users u ON u.id = lr.user_id
#             WHERE u.manager_id = ? AND lr.status = 'pending'
#             """,
#             (user["id"],),
#         ).fetchone()[0]
#         employee_count = db.execute(
#             "SELECT COUNT(*) FROM users WHERE manager_id = ?", (user["id"],)
#         ).fetchone()[0]
#     elif user["role"] == "admin":
#         team_pending = db.execute(
#             "SELECT COUNT(*) FROM leave_requests WHERE status = 'pending'"
#         ).fetchone()[0]
#         employee_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]

#     return jsonify(
#         {
#             "is_clocked_in": bool(open_attendance),
#             "clock_in_time": open_attendance["clock_in"] if open_attendance else None,
#             "own_pending_leaves": own_pending,
#             "onboarding": {"done": tasks_done, "total": tasks_total},
#             "review_queue": team_pending,
#             "employee_count": employee_count,
#         }
#     )


# @app.post("/api/attendance/toggle")
# @token_required
# def toggle_attendance():
#     db = get_db()
#     user_id = g.current_user["id"]
#     open_record = db.execute(
#         "SELECT * FROM attendance WHERE user_id = ? AND clock_out IS NULL ORDER BY id DESC LIMIT 1",
#         (user_id,),
#     ).fetchone()

#     if open_record:
#         clock_out = utc_now()
#         db.execute("UPDATE attendance SET clock_out = ? WHERE id = ?", (clock_out, open_record["id"]))
#         audit("CLOCK_OUT", "attendance", open_record["id"], f"Clocked out at {clock_out}")
#         db.commit()
#         return jsonify({"message": "Clocked out successfully.", "is_clocked_in": False})

#     clock_in = utc_now()
#     cursor = db.execute(
#         "INSERT INTO attendance (user_id, clock_in) VALUES (?, ?)", (user_id, clock_in)
#     )
#     audit("CLOCK_IN", "attendance", cursor.lastrowid, f"Clocked in at {clock_in}")
#     db.commit()
#     return jsonify(
#         {
#             "message": "Clocked in successfully.",
#             "is_clocked_in": True,
#             "clock_in_time": clock_in,
#         }
#     )


# @app.get("/api/attendance")
# @token_required
# def attendance_history():
#     rows = get_db().execute(
#         """
#         SELECT id, clock_in, clock_out
#         FROM attendance
#         WHERE user_id = ?
#         ORDER BY id DESC
#         LIMIT 20
#         """,
#         (g.current_user["id"],),
#     ).fetchall()
#     return jsonify([dict(row) for row in rows])


# @app.get("/api/leaves")
# @token_required
# def get_leaves():
#     db = get_db()
#     user = g.current_user

#     if user["role"] == "admin":
#         rows = db.execute(
#             """
#             SELECT lr.*, u.name AS employee_name, u.department
#             FROM leave_requests lr
#             JOIN users u ON u.id = lr.user_id
#             ORDER BY lr.id DESC
#             """
#         ).fetchall()
#     elif user["role"] == "manager":
#         rows = db.execute(
#             """
#             SELECT lr.*, u.name AS employee_name, u.department
#             FROM leave_requests lr
#             JOIN users u ON u.id = lr.user_id
#             WHERE lr.user_id = ? OR u.manager_id = ?
#             ORDER BY lr.id DESC
#             """,
#             (user["id"], user["id"]),
#         ).fetchall()
#     else:
#         rows = db.execute(
#             """
#             SELECT lr.*, u.name AS employee_name, u.department
#             FROM leave_requests lr
#             JOIN users u ON u.id = lr.user_id
#             WHERE lr.user_id = ?
#             ORDER BY lr.id DESC
#             """,
#             (user["id"],),
#         ).fetchall()

#     return jsonify([dict(row) for row in rows])


# @app.post("/api/leaves")
# @token_required
# def create_leave():
#     data = request.get_json(silent=True) or {}
#     required = ["leave_type", "start_date", "end_date", "reason"]
#     if any(not str(data.get(field, "")).strip() for field in required):
#         return jsonify({"error": "All leave request fields are required."}), 400

#     if data["end_date"] < data["start_date"]:
#         return jsonify({"error": "End date cannot be before start date."}), 400

#     db = get_db()
#     now = utc_now()
#     cursor = db.execute(
#         """
#         INSERT INTO leave_requests
#         (user_id, leave_type, start_date, end_date, reason, status, created_at, updated_at)
#         VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
#         """,
#         (
#             g.current_user["id"],
#             str(data["leave_type"]).strip(),
#             data["start_date"],
#             data["end_date"],
#             str(data["reason"]).strip(),
#             now,
#             now,
#         ),
#     )
#     audit("CREATE", "leave_request", cursor.lastrowid, "Submitted leave request")
#     db.commit()
#     return jsonify({"message": "Leave request submitted.", "id": cursor.lastrowid}), 201


# @app.patch("/api/leaves/<int:leave_id>/status")
# @roles_required("manager", "admin")
# def review_leave(leave_id: int):
#     data = request.get_json(silent=True) or {}
#     status = data.get("status")
#     note = str(data.get("note", "")).strip()

#     if status not in {"approved", "denied"}:
#         return jsonify({"error": "Status must be approved or denied."}), 400

#     db = get_db()
#     leave = db.execute("SELECT * FROM leave_requests WHERE id = ?", (leave_id,)).fetchone()
#     if not leave:
#         return jsonify({"error": "Leave request not found."}), 404
#     if leave["status"] != "pending":
#         return jsonify({"error": "Only pending leave requests can be reviewed."}), 409
#     if not user_can_review(leave["user_id"]):
#         return jsonify({"error": "You cannot review this employee's request."}), 403

#     db.execute(
#         """
#         UPDATE leave_requests
#         SET status = ?, reviewer_id = ?, reviewer_note = ?, updated_at = ?
#         WHERE id = ?
#         """,
#         (status, g.current_user["id"], note, utc_now(), leave_id),
#     )
#     audit("REVIEW", "leave_request", leave_id, f"Changed status to {status}")
#     db.commit()
#     return jsonify({"message": f"Leave request {status}."})


# @app.get("/api/onboarding")
# @token_required
# def get_onboarding():
#     rows = get_db().execute(
#         """
#         SELECT id, title, completed, completed_at
#         FROM onboarding_tasks
#         WHERE user_id = ?
#         ORDER BY id
#         """,
#         (g.current_user["id"],),
#     ).fetchall()
#     return jsonify([dict(row) for row in rows])


# @app.patch("/api/onboarding/<int:task_id>")
# @token_required
# def update_onboarding(task_id: int):
#     db = get_db()
#     task = db.execute(
#         "SELECT * FROM onboarding_tasks WHERE id = ? AND user_id = ?",
#         (task_id, g.current_user["id"]),
#     ).fetchone()
#     if not task:
#         return jsonify({"error": "Onboarding task not found."}), 404

#     completed = 0 if task["completed"] else 1
#     completed_at = utc_now() if completed else None
#     db.execute(
#         "UPDATE onboarding_tasks SET completed = ?, completed_at = ? WHERE id = ?",
#         (completed, completed_at, task_id),
#     )
#     audit("UPDATE", "onboarding_task", task_id, f"completed={completed}")
#     db.commit()
#     return jsonify({"message": "Onboarding task updated.", "completed": bool(completed)})


# @app.get("/api/okrs")
# @token_required
# def get_okrs():
#     rows = get_db().execute(
#         """
#         SELECT id, objective, key_result, progress, quarter, created_at
#         FROM okrs
#         WHERE user_id = ?
#         ORDER BY id DESC
#         """,
#         (g.current_user["id"],),
#     ).fetchall()
#     return jsonify([dict(row) for row in rows])


# @app.post("/api/okrs")
# @token_required
# def create_okr():
#     data = request.get_json(silent=True) or {}
#     objective = str(data.get("objective", "")).strip()
#     key_result = str(data.get("key_result", "")).strip()
#     quarter = str(data.get("quarter", "")).strip()
#     try:
#         progress = int(data.get("progress", 0))
#     except (TypeError, ValueError):
#         progress = -1

#     if not objective or not key_result or not quarter or not 0 <= progress <= 100:
#         return jsonify({"error": "Enter a valid objective, key result, quarter, and progress."}), 400

#     db = get_db()
#     cursor = db.execute(
#         """
#         INSERT INTO okrs (user_id, objective, key_result, progress, quarter, created_at)
#         VALUES (?, ?, ?, ?, ?, ?)
#         """,
#         (g.current_user["id"], objective, key_result, progress, quarter, utc_now()),
#     )
#     audit("CREATE", "okr", cursor.lastrowid, objective)
#     db.commit()
#     return jsonify({"message": "OKR saved.", "id": cursor.lastrowid}), 201


# @app.patch("/api/okrs/<int:okr_id>")
# @token_required
# def update_okr(okr_id: int):
#     data = request.get_json(silent=True) or {}
#     try:
#         progress = int(data.get("progress"))
#     except (TypeError, ValueError):
#         return jsonify({"error": "Progress must be a number from 0 to 100."}), 400

#     if not 0 <= progress <= 100:
#         return jsonify({"error": "Progress must be between 0 and 100."}), 400

#     db = get_db()
#     okr = db.execute(
#         "SELECT id FROM okrs WHERE id = ? AND user_id = ?",
#         (okr_id, g.current_user["id"]),
#     ).fetchone()
#     if not okr:
#         return jsonify({"error": "OKR not found."}), 404

#     db.execute("UPDATE okrs SET progress = ? WHERE id = ?", (progress, okr_id))
#     audit("UPDATE", "okr", okr_id, f"progress={progress}")
#     db.commit()
#     return jsonify({"message": "OKR progress updated."})


# @app.get("/api/employees")
# @roles_required("manager", "admin")
# def employees():
#     db = get_db()
#     if g.current_user["role"] == "admin":
#         rows = db.execute(
#             """
#             SELECT u.id, u.name, u.email, u.role, u.job_title, u.department,
#                    u.manager_id, m.name AS manager_name, u.leave_balance
#             FROM users u
#             LEFT JOIN users m ON m.id = u.manager_id
#             ORDER BY u.name
#             """
#         ).fetchall()
#     else:
#         rows = db.execute(
#             """
#             SELECT u.id, u.name, u.email, u.role, u.job_title, u.department,
#                    u.manager_id, m.name AS manager_name, u.leave_balance
#             FROM users u
#             LEFT JOIN users m ON m.id = u.manager_id
#             WHERE u.manager_id = ? OR u.id = ?
#             ORDER BY u.name
#             """,
#             (g.current_user["id"], g.current_user["id"]),
#         ).fetchall()
#     return jsonify([dict(row) for row in rows])


# @app.post("/api/employees")
# @roles_required("admin")
# def create_employee():
#     data = request.get_json(silent=True) or {}
#     required = ["name", "email", "password", "role", "job_title", "department"]
#     if any(not str(data.get(field, "")).strip() for field in required):
#         return jsonify({"error": "All employee fields are required."}), 400
#     if data["role"] not in {"admin", "manager", "employee"}:
#         return jsonify({"error": "Invalid role."}), 400

#     manager_id = data.get("manager_id") or None
#     db = get_db()
#     try:
#         cursor = db.execute(
#             """
#             INSERT INTO users
#             (name, email, password_hash, role, job_title, department, manager_id, leave_balance, created_at)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """,
#             (
#                 str(data["name"]).strip(),
#                 str(data["email"]).strip().lower(),
#                 generate_password_hash(str(data["password"])),
#                 data["role"],
#                 str(data["job_title"]).strip(),
#                 str(data["department"]).strip(),
#                 manager_id,
#                 int(data.get("leave_balance", 20)),
#                 utc_now(),
#             ),
#         )
#     except sqlite3.IntegrityError:
#         return jsonify({"error": "That email address is already in use."}), 409

#     user_id = cursor.lastrowid
#     default_tasks = [
#         "Complete employee profile",
#         "Read remote-work policy",
#         "Set up work environment",
#         "Meet direct manager",
#     ]
#     db.executemany(
#         "INSERT INTO onboarding_tasks (user_id, title) VALUES (?, ?)",
#         [(user_id, title) for title in default_tasks],
#     )
#     audit("CREATE", "user", user_id, str(data["email"]).strip().lower())
#     db.commit()
#     return jsonify({"message": "Employee created.", "id": user_id}), 201


# @app.delete("/api/employees/<int:user_id>")
# @roles_required("admin")
# def delete_employee(user_id: int):
#     if user_id == g.current_user["id"]:
#         return jsonify({"error": "You cannot delete your own account."}), 400

#     db = get_db()
#     user = db.execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchone()
#     if not user:
#         return jsonify({"error": "Employee not found."}), 404

#     # Detach direct reports before deleting a manager.
#     db.execute("UPDATE users SET manager_id = NULL WHERE manager_id = ?", (user_id,))
#     db.execute("DELETE FROM users WHERE id = ?", (user_id,))
#     audit("DELETE", "user", user_id, user["email"])
#     db.commit()
#     return jsonify({"message": "Employee removed."})


# @app.get("/api/audit")
# @roles_required("admin")
# def get_audit():
#     rows = get_db().execute(
#         """
#         SELECT a.id, a.action, a.entity_type, a.entity_id, a.details, a.created_at,
#                COALESCE(u.name, 'System') AS actor_name
#         FROM audit_logs a
#         LEFT JOIN users u ON u.id = a.actor_id
#         ORDER BY a.id DESC
#         LIMIT 100
#         """
#     ).fetchall()
#     return jsonify([dict(row) for row in rows])


# @app.errorhandler(404)
# def not_found(_error):
#     if request.path.startswith("/api/"):
#         return jsonify({"error": "API endpoint not found."}), 404
#     return send_from_directory(FRONTEND_DIR, "index.html")


# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True, host="127.0.0.1", port=5000)




import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth import hash_password
from database import Base, SessionLocal, engine
from models import Admin, CompanyDocument, Kudos, PerformanceReview
from routers import (
    analytics,
    announcements,
    attendance,
    dashboard,
    documents,
    employees,
    expenses,
    leave,
    login,
    okrs,
    onboarding,
    reviews,
    tasks,
)


# =========================================================
# Create default single Admin account
# =========================================================

def create_default_admin() -> None:
    """
    Create the default Admin account if it does not exist.
    """

    database = SessionLocal()

    try:
        default_accounts = [
            {
                "full_name": "System Administrator",
                "email": "admin@ems.local",
                "password": "Admin123!",
                "job_title": "Administrator",
                "department": "Administration",
            },
            {
                "full_name": "System Administrator",
                "email": "admin@gmail.com",
                "password": "Admin123",
                "job_title": "Administrator",
                "department": "Administration",
            },
            {
                "full_name": "Sarah Connor (Employee)",
                "email": "employee@gmail.com",
                "password": "Employee123",
                "job_title": "Frontend Developer",
                "department": "Engineering",
            },
            {
                "full_name": "Engineering Manager",
                "email": "manager@ems.local",
                "password": "Manager123!",
                "job_title": "Engineering Manager",
                "department": "Engineering",
            },
            {
                "full_name": "Michael Scott (Manager)",
                "email": "manager@gmail.com",
                "password": "Manager123",
                "job_title": "Regional Manager",
                "department": "Operations",
            },
            {
                "full_name": "Alex Rivera (Employee)",
                "email": "employee@ems.local",
                "password": "Employee123!",
                "job_title": "Software Engineer",
                "department": "Development",
            },
            {
                "full_name": "HR Operations Specialist",
                "email": "hr@gmail.com",
                "password": "HR123!",
                "job_title": "HR Manager",
                "department": "People Operations",
            },
                        {
                "full_name": "HR Operations Specialist 2",
                "email": "hr@gmail.com",
                "password": "HR1234!",
                "job_title": "HR Manager",
                "department": "People Operations",
            },
        ]

        for acc in default_accounts:
            existing = database.query(Admin).filter(Admin.email == acc["email"]).first()
            if not existing:
                user = Admin(
                    full_name=acc["full_name"],
                    email=acc["email"],
                    password_hash=hash_password(acc["password"]),
                    job_title=acc["job_title"],
                    department=acc["department"],
                    phone=None,
                    leave_balance=20,
                    is_active=True,
                )
                database.add(user)

        database.commit()

        # Seed initial Company Documents if table empty
        if database.query(CompanyDocument).count() == 0:
            docs = [
                CompanyDocument(
                    title="Employee Code of Conduct & Ethics",
                    category="Policy",
                    summary="Outlines standards for professional conduct, workplace equality, anti-harassment, and remote work integrity.",
                    version="v2.1",
                    requires_acknowledgment=True,
                ),
                CompanyDocument(
                    title="Remote & Hybrid Work Security Guidelines",
                    category="Security",
                    summary="Mandatory security standards regarding VPN usage, multi-factor authentication, password hygiene, and data protection.",
                    version="v1.4",
                    requires_acknowledgment=True,
                ),
                CompanyDocument(
                    title="Annual Leave & PTO Allowance Policy",
                    category="Benefits",
                    summary="Detailed guidelines on annual leave accrual, sick leave notifications, and request notice periods.",
                    version="v1.0",
                    requires_acknowledgment=True,
                ),
                CompanyDocument(
                    title="Expense Reimbursement & Travel Policy",
                    category="Finance",
                    summary="Eligible business expenses, submission deadlines, receipt requirements, and approval workflows.",
                    version="v3.0",
                    requires_acknowledgment=False,
                ),
            ]
            database.add_all(docs)

        # Seed initial Peer Kudos if table empty
        if database.query(Kudos).count() == 0:
            initial_kudos = [
                Kudos(
                    sender_name="Sarah Connor",
                    receiver_name="Alex Rivera",
                    category="Innovation",
                    message="Outstanding job automating the CI/CD pipeline! Saved the team hours every sprint.",
                ),
                Kudos(
                    sender_name="Michael Scott",
                    receiver_name="System Administrator",
                    category="Leadership",
                    message="Great leadership during the quarterly strategy meeting and smooth onboarding of new engineers.",
                ),
                Kudos(
                    sender_name="HR Operations",
                    receiver_name="Sarah Connor",
                    category="Teamwork",
                    message="Thank you for mentoring the new junior developers during their first week!",
                ),
            ]
            database.add_all(initial_kudos)

        # Seed initial Performance Review if table empty
        if database.query(PerformanceReview).count() == 0:
            admin_acc = database.query(Admin).first()
            if admin_acc:
                database.add(
                    PerformanceReview(
                        reviewer_id=admin_acc.id,
                        employee_id=admin_acc.id,
                        review_cycle="Q2 2026",
                        rating=5,
                        strengths="Exceptional leadership, prompt project execution, and strong technical initiative.",
                        growth_areas="Continue expanding cross-departmental documentation.",
                        status="completed",
                    )
                )

        database.commit()

        print("=" * 55)
        print("Default accounts created successfully:")
        for acc in default_accounts:
            print(f"- {acc['job_title']}: {acc['email']} / {acc['password']}")
        print("=" * 55)

    except Exception:
        database.rollback()
        raise

    finally:
        database.close()


# =========================================================
# Application startup
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create database tables and the default Admin account
    when the application starts.
    """

    Base.metadata.create_all(bind=engine)

    create_default_admin()

    yield


# =========================================================
# FastAPI application
# =========================================================

app = FastAPI(
    title="Remote Team and Employee Management Hub",
    description=(
        "Single-user Admin prototype for attendance, leave, "
        "onboarding tasks and personal OKRs."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


# =========================================================
# CORS configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Register API routers
# =========================================================

app.include_router(
    login.router,
    prefix="/api/auth",
    tags=["Authentication"],
)

app.include_router(
    attendance.router,
    prefix="/api/attendance",
    tags=["Attendance"],
)

app.include_router(
    dashboard.router,
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

app.include_router(
    leave.router,
    prefix="/api/leave",
    tags=["Leave"],
)

app.include_router(
    onboarding.router,
    prefix="/api/onboarding",
    tags=["Onboarding"],
)

app.include_router(
    okrs.router,
    prefix="/api/okrs",
    tags=["OKRs"],
)

app.include_router(
    tasks.router,
    prefix="/api/tasks",
    tags=["Tasks"],
)

app.include_router(
    announcements.router,
    prefix="/api/announcements",
    tags=["Announcements"],
)

app.include_router(
    expenses.router,
    prefix="/api/expenses",
    tags=["Payroll & Expenses"],
)

app.include_router(
    employees.router,
    prefix="/api/employees",
    tags=["Staff Directory"],
)

app.include_router(
    reviews.router,
    prefix="/api/reviews",
    tags=["Performance & Kudos"],
)

app.include_router(
    documents.router,
    prefix="/api/documents",
    tags=["Document Center"],
)

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["Analytics & Reports"],
)


# =========================================================
# Basic system routes
# =========================================================

@app.get("/")
def root():
    return {
        "application": "Remote Team and Employee Management Hub",
        "backend": "FastAPI",
        "prototype": "Single-user Admin",
        "status": "running",
        "documentation": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "message": "EMS backend is running successfully.",
    }


# =========================================================
# Start local development server
# =========================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )