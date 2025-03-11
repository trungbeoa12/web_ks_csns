from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from database import engine, SessionLocal
from auth import get_password_hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Hàm kết nối database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route đơn giản để test API hoạt động
@app.get("/")
def read_root():
    return {"Hello": "Khảo sát Project"}

# Tạo nhanh một user admin để test
@app.post("/create_admin/", response_model=schemas.UserResponse)
def create_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        role=user.role,
        branch_id=user.branch_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

