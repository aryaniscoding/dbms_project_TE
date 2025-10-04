from pydantic import BaseModel
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    role: str

    class Config:
        from_attributes = True

class SubjectOut(BaseModel):
    id: int
    code: str
    name: str
    credits: int
    teacher_id: Optional[int]
    class Config:
        from_attributes = True

class StudentOut(BaseModel):
    id: int
    student_code: str
    roll_no: str
    name: str
    division_id: Optional[int]
    batch: Optional[str]
    elective: Optional[str]
    class Config:
        from_attributes = True

class MarkIn(BaseModel):
    student_id: int
    subject_id: int
    marks: int

class MarkOut(BaseModel):
    subject_code: str
    subject_name: str
    marks: int
    grade: str
    grade_points: float

class ResultOut(BaseModel):
    student: StudentOut
    marks: List[MarkOut]
    cgpa: float
