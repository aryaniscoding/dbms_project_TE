import csv
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Student, Subject, Enrollment, Mark, RoleEnum
from app.utils import hash_password, grade_from_marks
from pathlib import Path

SUBJECTS = [
    ("CS101", "Programming Fundamentals", 4),
    ("MA101", "Mathematics I", 4),
    ("PH101", "Physics", 4),
    ("CH101", "Chemistry", 4),
    ("EN101", "English", 4),
]

TEACHERS = [
    ("teacher_cs", "Teacher CS", "cs@example.com"),
    ("teacher_ma", "Teacher MA", "ma@example.com"),
    ("teacher_ph", "Teacher PH", "ph@example.com"),
    ("teacher_ch", "Teacher CH", "ch@example.com"),
    ("teacher_en", "Teacher EN", "en@example.com"),
]

def ensure_admin(db: Session):
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(
            username="admin",
            full_name="Admin",
            email="admin@example.com",
            role=RoleEnum.admin,
            password_hash=hash_password("admin123"),
        )
        db.add(admin)
        db.commit()

def seed_subjects_and_teachers(db: Session):
    # subjects
    code_to_subj = {}
    for code, name, credits in SUBJECTS:
        subj = db.query(Subject).filter(Subject.code == code).first()
        if not subj:
            subj = Subject(code=code, name=name, credits=credits)
            db.add(subj)
            db.commit()
            db.refresh(subj)
        code_to_subj[code] = subj
    # teachers
    subj_ids = list(code_to_subj.values())
    for (username, full_name, email), subj in zip(TEACHERS, subj_ids):
        t = db.query(User).filter(User.username == username).first()
        if not t:
            t = User(username=username, full_name=full_name, email=email, role=RoleEnum.teacher, password_hash=hash_password("teacher123"))
            db.add(t)
            db.commit()
            db.refresh(t)
        subj.teacher_id = t.id
        db.commit()
    return code_to_subj

def seed_students(db: Session, csv_path: str):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scode = row["Student_Code"].strip()
            roll = str(row["Roll_No"]).strip()
            name = row["Name"].strip().strip('"')
            div = int(row["Division_ID"]) if row.get("Division_ID") else None
            batch = row.get("Batch") or None
            elective = row.get("Elective") or None
            if not db.query(Student).filter(Student.roll_no == roll).first():
                stu = Student(student_code=scode, roll_no=roll, name=name, division_id=div, batch=batch, elective=elective)
                db.add(stu)
                db.commit()
                db.refresh(stu)
                # create student user
                uname = f"s{roll}"
                if not db.query(User).filter(User.username == uname).first():
                    su = User(username=uname, full_name=name, role=RoleEnum.student, password_hash=hash_password("student123"), student_id=stu.id)
                    db.add(su)
                    db.commit()

def enroll_all_students_to_all_subjects(db: Session):
    subs = db.query(Subject).all()
    students = db.query(Student).all()
    for stu in students:
        for s in subs:
            exists = db.query(Enrollment).filter(Enrollment.student_id == stu.id, Enrollment.subject_id == s.id).first()
            if not exists:
                db.add(Enrollment(student_id=stu.id, subject_id=s.id))
    db.commit()

def seed_random_marks(db: Session):
    subs = db.query(Subject).all()
    students = db.query(Student).all()
    for stu in students:
        for s in subs:
            if not db.query(Mark).filter(Mark.student_id == stu.id, Mark.subject_id == s.id).first():
                marks_val = random.randint(35, 100)
                letter, gp = grade_from_marks(marks_val)
                # attribute to the assigned teacher if exists else admin(1)
                created_by = s.teacher_id or 1
                db.add(Mark(student_id=stu.id, subject_id=s.id, marks=marks_val, grade=letter, grade_points=gp, created_by=created_by))
    db.commit()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_admin(db)
        seed_subjects_and_teachers(db)
        # student_data.csv is at project root: backend/app/seed.py -> parents[2]
        csv_path = Path(__file__).resolve().parents[2] / "student_data.csv"
        seed_students(db, str(csv_path))
        enroll_all_students_to_all_subjects(db)
        seed_random_marks(db)
        print("Seeding complete:", csv_path)
    finally:
        db.close()
