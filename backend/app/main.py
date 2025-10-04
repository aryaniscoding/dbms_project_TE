from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User, RoleEnum
from .utils import verify_password
from .auth import create_access_token
from .schemas import LoginIn, Token, UserOut
from .routers import admin, teacher, student

app = FastAPI(title="Student Result Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.post("/auth/login", response_model=Token, tags=["auth"])
def login(payload: LoginIn):
    db: Session = SessionLocal()
    try:
        u = db.query(User).filter(User.username == payload.username).first()
        if not u or not verify_password(payload.password, u.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"sub": u.id, "role": u.role.value})
        return {"access_token": token, "token_type": "bearer"}
    finally:
        db.close()

@app.get("/auth/me", response_model=UserOut, tags=["auth"])
def me(token: str):
    # This endpoint is intentionally simple for demo, use /student/me etc. with auth guards for role routes
    db: Session = SessionLocal()
    try:
        u = db.query(User).filter(User.username == token).first()
        if not u:
            raise HTTPException(status_code=404, detail="Not found")
        return u
    finally:
        db.close()

app.include_router(admin.router)
app.include_router(teacher.router)
app.include_router(student.router)
