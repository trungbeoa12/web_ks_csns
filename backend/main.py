from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
import models, schemas, database
from database import engine, SessionLocal
from collections import Counter
import pandas as pd
import os
from passlib.context import CryptContext

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Cấu hình CORS để cho phép frontend truy cập API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kết nối database
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Băm mật khẩu với bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ============================
# 🚀 ROUTES - API
# ============================

# Kiểm tra server hoạt động
@app.get("/")
def read_root():
    return {"message": "Khảo sát Project đang chạy"}

# 🚀 API đăng nhập
@app.post("/login")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=400, detail="Sai tài khoản hoặc mật khẩu")
    
    return {"message": "Đăng nhập thành công", "username": user.username, "role": user.role}

# 🚀 API tạo user mới (chỉ dùng để thêm user)
@app.post("/create_user/")
async def create_user(username: str, password: str, role: str = "branch", branch_id: int = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return {"error": "User đã tồn tại!"}
    
    new_user = models.User(
        username=username,
        password_hash=get_password_hash(password),
        role=role,
        branch_id=branch_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user": {"username": username, "role": role}}

# 🚀 API nhận dữ liệu khảo sát từ frontend
@app.post("/submit_survey/")
async def submit_survey(survey_data: dict, db: Session = Depends(get_db)):
    new_survey = models.SurveyResponse(
        branch_id=1,  # 🔥 Tạm thời đặt branch_id là 1, sau này lấy từ user đăng nhập
        
        q1="Đầu tư trụ sở mới" in survey_data["csvc"],
        q2="Áp dụng mô hình sảnh giao dịch chuẩn" in survey_data["csvc"],
        q3="Trang bị máy R-ATM" in survey_data["csvc"],
        q4="Trang bị hệ thống lấy số tự động" in survey_data["csvc"],
        q5=survey_data["csvc_khac"],

        q6="Nâng mức thẩm quyền cấp tín dụng" in survey_data["csqd"],
        q7="Nâng mức thẩm quyền giải ngân" in survey_data["csqd"],
        q8="Nâng hạn mức phê duyệt giao dịch" in survey_data["csqd"],
        q9="Có các sản phẩm đặc thù dành riêng" in survey_data["csqd"],
        q10="Cơ chế hỗ trợ khác" in survey_data["csqd"],
        q11=survey_data["csqd_khac"]
    )
    
    db.add(new_survey)
    db.commit()
    db.refresh(new_survey)
    return {"message": "Khảo sát đã được lưu!", "survey_id": new_survey.id}

# 🚀 API lấy dữ liệu thống kê Dashboard
@app.get("/dashboard_data/")
async def get_dashboard_data(branch_id: int = None, db: Session = Depends(get_db)):
    if branch_id:
        surveys = db.query(models.SurveyResponse).filter(models.SurveyResponse.branch_id == branch_id).all()
    else:
        surveys = db.query(models.SurveyResponse).all()

    # Thống kê số lượng câu trả lời
    stats = {
        "q1": sum(s.q1 for s in surveys),
        "q2": sum(s.q2 for s in surveys),
        "q3": sum(s.q3 for s in surveys),
        "q4": sum(s.q4 for s in surveys),
        "q5": [s.q5 for s in surveys if s.q5 and s.q5.strip()],
        "q6": sum(s.q6 for s in surveys),
        "q7": sum(s.q7 for s in surveys),
        "q8": sum(s.q8 for s in surveys),
        "q9": sum(s.q9 for s in surveys),
        "q10": sum(s.q10 for s in surveys),
        "q11": [s.q11 for s in surveys if s.q11 and s.q11.strip()],
    }

    return JSONResponse(content=stats)


# 🚀 API xuất dữ liệu khảo sát ra file Excel
@app.get("/export_excel/")
async def export_excel(db: Session = Depends(get_db)):
    surveys = db.query(models.SurveyResponse).all()

    data = {
        "Q1": [s.q1 for s in surveys],
        "Q2": [s.q2 for s in surveys],
        "Q3": [s.q3 for s in surveys],
        "Q4": [s.q4 for s in surveys],
        "Ý kiến khác Q5": [s.q5 for s in surveys if s.q5],
        "Q6": [s.q6 for s in surveys],
        "Q7": [s.q7 for s in surveys],
        "Q8": [s.q8 for s in surveys],
        "Ý kiến khác Q11": [s.q11 for s in surveys if s.q11]
    }

    df = pd.DataFrame(data)
    
    EXPORT_DIR = os.path.join(os.getcwd(), "backend", "exports")
    os.makedirs(EXPORT_DIR, exist_ok=True)  # Đảm bảo thư mục tồn tại

    file_path = os.path.join(EXPORT_DIR, "survey_results.xlsx")

    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename="survey_results.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
from fastapi import HTTPException

@app.get("/user_info/")
async def get_user_info(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User không tồn tại")
    
    return {"username": user.username, "role": user.role, "branch_id": user.branch_id}


