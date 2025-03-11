from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

# 🔥 Định nghĩa app ở ĐÂY trước khi thêm middleware
app = FastAPI()

# ✅ Thêm middleware CORS đúng chỗ, ngay sau khi khởi tạo app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả frontend kết nối
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Hàm kết nối database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔥 Route test API
@app.get("/")
def read_root():
    return {"message": "Khảo sát Project đang chạy"}

# 🔥 API nhận dữ liệu khảo sát từ frontend
@app.post("/submit_survey/")
async def submit_survey(survey_data: dict):
    print("Dữ liệu nhận được:", survey_data)  # Debug log
    return {"message": "Khảo sát đã được ghi nhận!", "data": survey_data}

