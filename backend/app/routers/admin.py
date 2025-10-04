from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..deps import get_db, require_role
from ..models import User, RoleEnum, Subject, Student, Enrollment
from ..schemas import SubjectOut, UserOut
from ..utils import hash_password

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/subjects", response_model=List[SubjectOut])
def list_subjects(db: Session = Depends(get_db), _: User = Depends(require_role(RoleEnum.admin))):
    return db.query(Subject).all()

@router.post("/subjects", response_model=SubjectOut)
def create_subject(code: str, name: str, credits: int = 4, db: Session = Depends(get_db), _: User = Depends(require_role(RoleEnum.admin))):
    if db.query(Subject).filter(Subject.code == code).first():
        raise HTTPException(status_code=400, detail="Subject code exists")
    s = Subject(code=code, name=name, credits=credits)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.post("/assign-teacher")
def assign_teacher(subject_id: int, teacher_user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role(RoleEnum.admin))):
    subj = db.query(Subject).filter(Subject.id == subject_id).first()
    teacher = db.query(User).filter(User.id == teacher_user_id, User.role == RoleEnum.teacher).first()
    if not subj or not teacher:
        raise HTTPException(status_code=404, detail="Subject or teacher not found")
    subj.teacher_id = teacher.id
    db.commit()
    return {"status": "ok"}

@router.get("/students", response_model=List[UserOut])
def list_student_users(db: Session = Depends(get_db), _: User = Depends(require_role(RoleEnum.admin))):
    users = db.query(User).filter(User.role == RoleEnum.student).all()
    return users

@router.post("/create-user", response_model=UserOut)
def create_user(username: str, password: str, role: RoleEnum, full_name: Optional[str] = None, email: Optional[str] = None,
                student_id: Optional[int] = None,
                db: Session = Depends(get_db), _: User = Depends(require_role(RoleEnum.admin))):
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username exists")
    if role == RoleEnum.student and not student_id:
        raise HTTPException(status_code=400, detail="student_id required for student role")
    u = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
        full_name=full_name,
        email=email,
        student_id=student_id
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u
