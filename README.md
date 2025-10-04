# Student Result Management System (SRMS)

A full-stack, DBMS‑centered web app for uploading, storing, and viewing student examination results with CGPA and grade calculation, featuring role-based access for admin, teacher, and student.

### What this project does
- Stores students, subjects, enrollments, and marks in MySQL with strict integrity and unique constraints.
- Enforces three roles: admin (full access), teacher (enter/update marks only for assigned subject), student (view personal results only).
- Calculates per-subject letter grades and overall CGPA using a 10‑point scale shown to two decimals.
- Seeds the database from a provided CSV of students and generates random marks for five default subjects.
- Presents a neon/animated HTML/CSS/JS frontend and a FastAPI backend secured with JWT.

### Tech stack
- Backend: FastAPI, Uvicorn, SQLAlchemy, PyMySQL, Passlib (password hashing), JWT
- Database: MySQL 8.x
- Frontend: HTML, CSS (neon styles), Vanilla JS
- Auth: JWT bearer authentication with role guards and password hashing
- Data seeding: CSV ingestion plus randomized marks for five subjects

### CGPA and grading
- Grade points mapping: 90–100 → 10, 80–89 → 9, 70–79 → 8, 60–69 → 7, 50–59 → 6, 40–49 → 5, else 0 (letters: O, A+, A, B+, B, C, F).
- CGPA formula for five subjects: $$ \mathrm{CGPA} = \frac{\mathrm{GP}_1 + \mathrm{GP}_2 + \mathrm{GP}_3 + \mathrm{GP}_4 + \mathrm{GP}_5}{5} $$.

### Role capabilities

| Role     | Capabilities |
|----------|--------------|
| Admin    | Manage users, create subjects, assign teacher to subject, full data visibility and control |
| Teacher  | View assigned subject, create/update marks only for the assigned subject |
| Student  | View personal profile, marks across five subjects, letter grades, and CGPA |

### Project structure

```
student-result-system/
├─ backend/
│  ├─ app/
│  │  ├─ __init__.py
│  │  ├─ main.py
│  │  ├─ config.py
│  │  ├─ database.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ auth.py
│  │  ├─ utils.py
│  │  ├─ deps.py
│  │  └─ routers/
│  │     ├─ __init__.py
│  │     ├─ admin.py
│  │     ├─ teacher.py
│  │     └─ student.py
│  ├─ seed.py
│  ├─ requirements.txt
│  └─ .env.example
├─ frontend/
│  ├─ index.html
│  ├─ admin.html
│  ├─ teacher.html
│  ├─ student.html
│  ├─ css/
│  │  ├─ styles.css
│  │  └─ neon.css
│  └─ js/
│     ├─ api.js
│     ├─ auth.js
│     ├─ admin.js
│     ├─ teacher.js
│     ├─ student.js
│     ├─ ui.js
│     └─ particles.js
├─ sql/
│  └─ init.sql
├─ student_data.csv
└─ README.md
```

### Backend modules (quick map)
- config.py: reads environment variables for DB connection and JWT settings.
- database.py: SQLAlchemy engine, session, and Base.
- models.py: ORM models (User, Student, Subject, Enrollment, Mark) and role enum.
- schemas.py: Pydantic request/response models.
- auth.py: JWT create/decode helpers.
- deps.py: DB session dependency and role-based guards.
- routers/admin.py: subject CRUD, teacher assignment, user creation, student user listing.
- routers/teacher.py: assigned-subject lookup, create/update marks for assigned subject.
- routers/student.py: student profile and personal results with CGPA.
- seed.py: creates admin, teachers, subjects, students from CSV, enrollments, and random marks.

### Frontend pages
- index.html: login with JWT; routes to role dashboards based on token payload.
- admin.html: create subjects/users, assign teacher to subject, list student users.
- teacher.html: view assigned subject, submit/update marks for that subject.
- student.html: view profile, per-subject marks, letter grades, and CGPA.

***

## Getting started

### Prerequisites
- Python 3.11+ (works on 3.13; ensure a virtual environment is used)
- MySQL 8.x installed locally and the Windows service running (MySQL80 on Windows)
- Node is not required (pure HTML/CSS/JS frontend)

### 1) Create the database
- Option A: run the SQL initializer
  - Use MySQL CLI or Workbench and execute:
    - CREATE DATABASE IF NOT EXISTS srms_db;
- Option B: run sql/init.sql

### 2) Configure environment
- Copy backend/.env.example to backend/.env and update values:
  - MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST=127.0.0.1, MYSQL_PORT=3306, MYSQL_DB=srms_db
  - SECRET_KEY=any long random string
  - ACCESS_TOKEN_EXPIRE_MINUTES=120

Example .env
```
MYSQL_USER=srms_user
MYSQL_PASSWORD=StrongPass!123
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=srms_db
SECRET_KEY=change_this_secret
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

Tip: Prefer a scoped application user instead of root:
- CREATE USER 'srms_user'@'localhost' IDENTIFIED BY 'StrongPass!123';
- GRANT ALL PRIVILEGES ON srms_db.* TO 'srms_user'@'localhost';
- FLUSH PRIVILEGES;

### 3) Install backend dependencies
From the backend folder:
- Create and activate a virtual environment.
- Install:
  - pip install -r requirements.txt

If encountering bcrypt backend issues on Windows/Python 3.13, switch to PBKDF2 in backend/app/utils.py:
```
from passlib.context import CryptContext
pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], default="pbkdf2_sha256")
```
Then change requirements.txt to use passlib==1.7.4 (without the bcrypt extra), and reinstall.

If connecting to MySQL 8 fails with “cryptography required”, install one of:
- pip install cryptography
- pip install "PyMySQL[rsa]"

### 4) Initialize tables and run the API
From the backend folder:
- Start the API:
  - uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
- Visit http://127.0.0.1:8000/docs to check endpoints.

If MySQL service isn’t running, start it:
- Windows Services → MySQL80 → Start
- Or command prompt (admin): net start MySQL80

### 5) Seed data (students, subjects, enrollments, marks)
There are two reliable ways:

- Option A (module execution from backend folder):
  - python -m app.seed
  - This expects student_data.csv at the project root; if needed, update seed.py to resolve the CSV path via Path(__file__).resolve().parents / "student_data.csv".[9]

- Option B (run from project root):
  - python backend\seed.py
  - This uses the relative path "student_data.csv" at the root.

Seeding creates:
- Admin user: admin / admin123
- Five teachers: teacher_cs, teacher_ma, teacher_ph, teacher_ch, teacher_en (all with teacher123)
- Students from CSV: username is s{Roll_No} with password student123
- Five subjects with one teacher assigned to each
- Global enrollments and random marks for each student across five subjects

### 6) Run the frontend
- Open frontend/index.html in a browser (or serve the folder with any static server).
- Log in with one of the demo accounts:
  - Admin: admin / admin123
  - Teacher: teacher_cs / teacher123 (others similar)
  - Student: s{Roll_No} / student123 (for example s32107)

### 7) API quick reference
- POST /auth/login: obtain JWT
- GET /admin/subjects, POST /admin/subjects: list/create subjects (admin)
- POST /admin/assign-teacher: assign teacher to subject (admin)
- GET /admin/students: list student users (admin)
- GET /teacher/my-subject: see assigned subject (teacher)
- POST /teacher/marks: create/update mark for assigned subject (teacher)
- GET /student/me: student profile (student)
- GET /student/me/marks: personal marks and CGPA (student)

***

## Troubleshooting

- Address/host errors while starting Uvicorn
  - Use a valid host such as 127.0.0.1 or 0.0.0.0.
  - From backend, the correct app import path is app.main:app.

- “attempted relative import with no known parent package”
  - Launch from backend using app.main:app or run modules as python -m app.seed.

- MySQL service not running or cannot connect
  - Ensure the MySQL80 service is started.
  - Verify credentials via mysql -h 127.0.0.1 -u <user> -p.
  - Confirm port 3306 is free or adjust MYSQL_PORT.

- MySQL 8 authentication failures
  - Install cryptography or PyMySQL with RSA extra.
  - Optionally set the app user to mysql_native_password for local dev.

- FileNotFoundError for student_data.csv
  - Run seeder from the project root (python backend\seed.py), or resolve an absolute path from __file__ in seed.py, or move the CSV next to seed.py and adjust the path.

- Passlib bcrypt issues on Windows/Python 3.13
  - Prefer pbkdf2_sha256 in utils.py and remove bcrypt extras from requirements, or pin bcrypt to a compatible version if wheels exist for the interpreter.

***

## Security notes

- Do not use demo passwords in production.
- Regenerate SECRET_KEY and reduce allowed origins for CORS.
- Scope database permissions to the application database and user.
- Consider HTTPS, secure cookie storage for tokens, and stricter password policies.

***

