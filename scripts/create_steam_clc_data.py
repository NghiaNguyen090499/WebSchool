"""
Script tạo dữ liệu mẫu cho hệ STEAM Chất lượng cao
Run: python manage.py shell < scripts/create_steam_clc_data.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from core.models import TrainingProgram

# Dữ liệu cho hệ STEAM Chất lượng cao
steam_clc_data = {
    'program_type': 'steam_clc',
    'short_name': 'Hệ STEAM Chất lượng cao',
    'full_name': 'Hệ STEAM Chất lượng cao - Công nghệ tiên tiến',
    'tagline': 'Chương trình giáo dục STEAM chất lượng cao với chuẩn quốc tế, trang bị cho học sinh tư duy sáng tạo, kỹ năng giải quyết vấn đề và năng lực công nghệ vượt trội.',
    'description': '''Hệ STEAM Chất lượng cao tại MIS là chương trình giáo dục đặc biệt được thiết kế dành cho những học sinh có đam mê và năng khiếu trong các lĩnh vực Khoa học, Công nghệ, Kỹ thuật, Nghệ thuật và Toán học.

Chương trình được xây dựng theo chuẩn quốc tế với:
• Giáo viên chuyên gia được đào tạo từ các trường đại học hàng đầu
• Phòng thí nghiệm và trang thiết bị hiện đại
• Hợp tác với các doanh nghiệp công nghệ hàng đầu
• Cơ hội tham gia các cuộc thi quốc tế về STEM/STEAM

Học sinh sẽ được học tập trong môi trường sáng tạo, được thực hành với các dự án thực tế và phát triển kỹ năng làm việc nhóm, tư duy phản biện.''',
    'curriculum': '''📚 CHƯƠNG TRÌNH HỌC:

🔬 KHOA HỌC (Science):
• Vật lý ứng dụng và thí nghiệm
• Hóa học và công nghệ vật liệu mới
• Sinh học và công nghệ sinh học

💻 CÔNG NGHỆ (Technology):
• Lập trình Python, JavaScript, AI cơ bản
• Thiết kế 3D và in 3D
• Internet of Things (IoT)

⚙️ KỸ THUẬT (Engineering):
• Robotics nâng cao
• Điện tử cơ bản và mạch điện
• Thiết kế sản phẩm

🎨 NGHỆ THUẬT (Art):
• Thiết kế đồ họa
• Video editing và Animation
• Tư duy thiết kế (Design Thinking)

📐 TOÁN HỌC (Math):
• Toán tư duy và giải toán sáng tạo
• Thống kê và phân tích dữ liệu
• Toán ứng dụng trong công nghệ''',
    'highlights': '''Chương trình chuẩn quốc tế với giáo trình tiên tiến
Phòng lab hiện đại với trang thiết bị công nghệ cao
Giáo viên chuyên gia, nhiều năm kinh nghiệm
Học qua dự án thực tế (Project-Based Learning)
Tham gia các cuộc thi STEM/STEAM quốc gia và quốc tế
Cơ hội thực tập tại doanh nghiệp công nghệ
Chứng chỉ quốc tế được công nhận
Kết nối với cộng đồng STEAM toàn cầu''',
    'partner_name': 'Viện Công nghệ Giáo dục Việt Nam',
    'grade_levels': 'Lớp 6 - Lớp 12',
    'icon': 'fas fa-rocket',
    'color': 'orange',
    'is_active': True,
    'order': 1,
}

# Tạo hoặc cập nhật
program, created = TrainingProgram.objects.update_or_create(
    program_type='steam_clc',
    defaults=steam_clc_data
)

if created:
    print(f"✅ Đã tạo mới: {program.short_name}")
else:
    print(f"✅ Đã cập nhật: {program.short_name}")

# Hiển thị tất cả các hệ đào tạo hiện có
print("\n📋 Danh sách các hệ đào tạo:")
for p in TrainingProgram.objects.all().order_by('order'):
    print(f"   - {p.get_program_type_display()} ({p.program_type})")
