from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import models, schemas, database
from database import engine, SessionLocal
from collections import Counter
import pandas as pd
import os
from fastapi.responses import FileResponse

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
    
@app.get("/dashboard_data/")
async def get_dashboard_data(db: Session = Depends(get_db)):
    surveys = db.query(models.SurveyResponse).all()
    
    # Thống kê số lượng câu trả lời
    stats = {
        "q1": sum(s.q1 for s in surveys),
        "q2": sum(s.q2 for s in surveys),
        "q3": sum(s.q3 for s in surveys),
        "q4": sum(s.q4 for s in surveys),
        "q5": [s.q5 for s in surveys if s.q5 and s.q5.strip()],  # Lọc giá trị trống
        "q6": sum(s.q6 for s in surveys),
        "q7": sum(s.q7 for s in surveys),
        "q8": sum(s.q8 for s in surveys),
        "q9": sum(s.q9 for s in surveys),
        "q10": sum(s.q10 for s in surveys),
        "q11": [s.q11 for s in surveys if s.q11 and s.q11.strip()],  # Lọc giá trị trống
    }

    return JSONResponse(content=stats)

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


