from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Float, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    full_name = Column(String(128), nullable=True)
    email = Column(String(128), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="user", uselist=False)
    subjects = relationship("Subject", back_populates="teacher")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_code = Column(String(64), unique=True, index=True, nullable=False)
    roll_no = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(128), index=True, nullable=False)
    division_id = Column(Integer, nullable=True)
    batch = Column(String(16), nullable=True)
    elective = Column(String(32), nullable=True)

    user = relationship("User", back_populates="student", uselist=False)
    enrollments = relationship("Enrollment", back_populates="student")
    marks = relationship("Mark", back_populates="student")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), unique=True, index=True, nullable=False)
    name = Column(String(128), nullable=False)
    credits = Column(Integer, nullable=False, default=4)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    teacher = relationship("User", back_populates="subjects")
    enrollments = relationship("Enrollment", back_populates="subject")
    marks = relationship("Mark", back_populates="subject")

class Enrollment(Base):
    __tablename__ = "enrollments"
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), primary_key=True)

    student = relationship("Student", back_populates="enrollments")
    subject = relationship("Subject", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", name="uq_student_subject"),
    )

class Mark(Base):
    __tablename__ = "marks"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), index=True, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), index=True, nullable=False)
    marks = Column(Integer, nullable=False)  # 0-100
    grade = Column(String(4), nullable=False)
    grade_points = Column(Float, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # teacher user id
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject", back_populates="marks")

    __table_args__ = (
        UniqueConstraint("student_id", "subject_id", name="uq_mark_per_subject"),
    )
