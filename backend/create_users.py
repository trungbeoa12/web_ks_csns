from sqlalchemy.orm import Session
import models, database
from main import get_password_hash
import random
import string

db: Session = database.SessionLocal()

def generate_password(length=10):
    """Sinh mật khẩu ngẫu nhiên."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ✅ Tạo user admin
admin_password = generate_password(12)  # 🔥 Mật khẩu admin 12 ký tự
admin = models.User(
    username="admin",
    password_hash=get_password_hash(admin_password),
    plain_password=admin_password,  # 🔥 Lưu vào DB để dễ copy (tùy chọn)
    role="admin"
)
db.add(admin)
print(f"✅ User admin đã tạo! Mật khẩu: {admin_password}")

# ✅ Danh sách chi nhánh
branch_ids = [
    106, 122, 124, 126, 127, 128, 129, 131, 136, 140, 142, 144, 145, 146, 160, 161, 162, 164, 166, 168, 
    169, 170, 172, 174, 180, 182, 184, 186, 188, 189, 190, 195, 200, 220, 222, 224, 240, 242, 244, 246, 
    248, 250, 260, 262, 264, 280, 282, 284, 285, 289, 300, 302, 304, 306, 308, 316, 320, 322, 324, 326, 
    328, 333, 340, 342, 343, 344, 346, 360, 380, 382, 384, 400, 402, 420, 422, 424, 430, 440, 441, 442, 
    444, 450, 460, 462, 470, 480, 482, 484, 486, 488, 490, 500, 502, 504, 506, 510, 520, 540, 542, 560, 
    580, 600, 610, 620, 622, 640, 660, 662, 664, 680, 681, 682, 700, 704, 720, 724, 740, 742, 760, 762, 
    780, 800, 820, 821, 822, 824, 840, 842, 860, 862, 880, 900, 901, 902, 903, 904, 906, 908, 910, 912, 
    920, 922, 923, 924, 926, 928, 930, 932, 940, 942, 944, 945, 946, 947, 948, 980
]

# ✅ Tạo user cho từng chi nhánh
for branch_id in branch_ids:
    branch_password = generate_password(10)  # 🔥 Mật khẩu chi nhánh 10 ký tự
    user = models.User(
        username=f"branch_{branch_id}",
        password_hash=get_password_hash(branch_password),
        plain_password=branch_password,  # 🔥 Lưu mật khẩu gốc (tùy chọn)
        role="branch",
        branch_id=branch_id
    )
    db.add(user)
    print(f"✅ User branch_{branch_id} đã tạo! Mật khẩu: {branch_password}")

db.commit()
db.close()

print("\n🎉 Đã tạo user admin và 155 user chi nhánh thành công!")

