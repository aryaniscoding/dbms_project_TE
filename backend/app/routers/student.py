from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from statistics import mean
from ..deps import get_db, require_role, get_current_user
from ..models import User, RoleEnum, Student, Mark, Subject
from ..schemas import ResultOut, MarkOut, StudentOut

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/me", response_model=StudentOut)
def me(db: Session = Depends(get_db), user: User = Depends(require_role(RoleEnum.student))):
    if not user.student_id:
        raise HTTPException(status_code=404, detail="No student profile")
    stu = db.query(Student).filter(Student.id == user.student_id).first()
    return stu

@router.get("/me/marks", response_model=ResultOut)
def my_marks(db: Session = Depends(get_db), user: User = Depends(require_role(RoleEnum.student))):
    stu = db.query(Student).filter(Student.id == user.student_id).first()
    if not stu:
        raise HTTPException(status_code=404, detail="No student profile")
    marks = db.query(Mark, Subject).join(Subject, Subject.id == Mark.subject_id).filter(Mark.student_id == stu.id).all()
    mark_list = [MarkOut(subject_code=s.code, subject_name=s.name, marks=m.marks, grade=m.grade, grade_points=m.grade_points) for (m, s) in marks]
    gp = [m.grade_points for m, _ in marks]
    cgpa = round(mean(gp), 2) if gp else 0.0
    return {"student": stu, "marks": mark_list, "cgpa": cgpa}
