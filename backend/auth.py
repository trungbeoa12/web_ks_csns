from passlib.context import CryptContext

# Cấu hình bcrypt để mã hóa mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hàm mã hóa mật khẩu
def get_password_hash(password):
    return pwd_context.hash(password)

# Hàm kiểm tra mật khẩu nhập vào có đúng không
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

