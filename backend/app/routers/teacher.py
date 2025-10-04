from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, require_role, get_current_user
from ..models import User, RoleEnum, Subject, Mark, Student
from ..schemas import MarkIn
from ..utils import grade_from_marks

router = APIRouter(prefix="/teacher", tags=["teacher"])

def _get_teacher_subject(db: Session, teacher_id: int) -> Subject:
    subj = db.query(Subject).filter(Subject.teacher_id == teacher_id).first()
    return subj

@router.get("/my-subject")
def my_subject(db: Session = Depends(get_db), user: User = Depends(require_role(RoleEnum.teacher))):
    subj = _get_teacher_subject(db, user.id)
    if not subj:
        return {"message": "No subject assigned"}
    return {"id": subj.id, "code": subj.code, "name": subj.name}

@router.post("/marks")
def create_or_update_mark(payload: MarkIn, db: Session = Depends(get_db), user: User = Depends(require_role(RoleEnum.teacher))):
    subj = _get_teacher_subject(db, user.id)
    if not subj or subj.id != payload.subject_id:
        raise HTTPException(status_code=403, detail="Teacher can only submit marks for assigned subject")
    stu = db.query(Student).filter(Student.id == payload.student_id).first()
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    letter, gp = grade_from_marks(payload.marks)
    existing = db.query(Mark).filter(Mark.student_id == stu.id, Mark.subject_id == subj.id).first()
    if existing:
        existing.marks = payload.marks
        existing.grade = letter
        existing.grade_points = gp
    else:
        m = Mark(student_id=stu.id, subject_id=subj.id, marks=payload.marks, grade=letter, grade_points=gp, created_by=user.id)
        db.add(m)
    db.commit()
    return {"status": "ok"}
