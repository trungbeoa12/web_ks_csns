from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# 🔥 Bảng chứa thông tin các Chi nhánh
class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Quan hệ 1-n với User
    users = relationship("User", back_populates="branch", cascade="all, delete-orphan")
    # Quan hệ 1-n với SurveyResponse
    surveys = relationship("SurveyResponse", back_populates="branch", cascade="all, delete-orphan")

# 🔥 Bảng chứa thông tin các user đăng nhập (Admin và Chi nhánh)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Mật khẩu đã hash
    plain_password = Column(String, nullable=True)  # 🚨 Lưu mật khẩu gốc (Chỉ dùng để dễ quản lý)
    role = Column(String, default="branch")  # "admin" hoặc "branch"
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=True)

    # Quan hệ với Branch
    branch = relationship("Branch", back_populates="users")

# 🔥 Bảng chứa kết quả khảo sát
class SurveyResponse(Base):
    __tablename__ = "survey_responses"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Lưu các câu trả lời dạng tích chọn (checkbox)
    q1 = Column(Boolean, default=False)
    q2 = Column(Boolean, default=False)
    q3 = Column(Boolean, default=False)
    q4 = Column(Boolean, default=False)
    q5 = Column(String, nullable=True)

    q6 = Column(Boolean, default=False)
    q7 = Column(Boolean, default=False)
    q8 = Column(Boolean, default=False)
    q9 = Column(Boolean, default=False)
    q10 = Column(Boolean, default=False)
    q11 = Column(String, nullable=True)

    q12 = Column(Boolean, default=False)
    q13 = Column(Boolean, default=False)
    q14 = Column(Boolean, default=False)
    q15 = Column(Boolean, default=False)
    q16 = Column(Boolean, default=False)
    q17 = Column(String, nullable=True)

    # Các câu hỏi thêm ở cuối khảo sát
    implement_super_pgd = Column(Boolean, default=False)
    proposed_pgd_info = Column(String, nullable=True)
    other_banks_info = Column(String, nullable=True)
    other_comments = Column(String, nullable=True)

    # Quan hệ với Branch
    branch = relationship("Branch", back_populates="surveys")

