from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Đường dẫn database SQLite (cho dễ quản lý ban đầu, không cần cài thêm gì)
DATABASE_URL = "sqlite:///./survey.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Tạo session để tương tác database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base dùng để tạo model
Base = declarative_base()

