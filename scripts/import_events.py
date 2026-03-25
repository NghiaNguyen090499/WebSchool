"""
Script to populate events from the school activity plan (docx file).
Run with: python manage.py shell < scripts/import_events.py
"""
import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from datetime import date
from django.utils.text import slugify
from events.models import Event

events_data = [
    # ═══════════════ THÁNG 3/2026 — Non sông gấm vóc ═══════════════
    {
        "title": "Phát động phong trào chào mừng ngày 8/3",
        "date": date(2026, 3, 2),
        "location": "Toàn trường",
        "description": (
            "Các bài viết hoặc các tác phẩm nghệ thuật dành cho: Các bà, các mẹ, vợ, các cô. "
            "Radio: Thông điệp yêu thương, hát về mẹ. "
            "Phát huy tinh thần yêu thương, tôn trọng đối với một nửa thế giới."
        ),
    },
    {
        "title": 'Chung kết Flashmob "Dance Talent of MIS"',
        "date": date(2026, 3, 6),
        "location": "Sân trường MIS",
        "description": (
            "Lựa chọn ra các Giải thưởng tài năng của học sinh, "
            "biểu diễn các tiết mục chào mừng ngày Quốc tế Phụ nữ 8/3. "
            "Đơn vị đảm nhiệm: TPT, Khối VĐNT-TNHT."
        ),
    },
    {
        "title": "Kỷ niệm ngày Quốc tế Phụ nữ 8/3",
        "date": date(2026, 3, 6),
        "location": "Hội trường Grace",
        "description": (
            '"Phụ Nữ Hạnh Phúc – Thế Giới Hạnh Phúc". '
            "Cuộc thi hát, thơ, bình video về mẹ bằng cả tiếng Anh, Trung, Việt. "
            "Tri ân Mẹ, lấy video tổ chức chấm theo hình thức online, "
            "đa dạng năng khiếu ngoại ngữ. "
            "Đơn vị đảm nhiệm: TPT, Ban TTTS, GVCN."
        ),
    },
    {
        "title": "Khởi động MIS Dubbing Challenge & Dự án liên môn KHXH",
        "date": date(2026, 3, 10),
        "location": "Toàn trường",
        "description": (
            "Khởi động MIS Dubbing Challenge – Cuộc thi lồng tiếng Anh. "
            "Khởi động dự án Tích hợp liên môn KHXH. "
            "Đơn vị đảm nhiệm: Khối Ngoại Ngữ, GVCN."
        ),
    },
    {
        "title": "MIS Championship Connect & Compete – Hội thao CBCNV-GV-PHHS-HS",
        "date": date(2026, 3, 2),
        "location": "Sân vận động MIS",
        "description": (
            "Hoạt động chào mừng ngày thành lập Đoàn TNCS HCM. "
            "Cùng nhau tạo những kỷ niệm và luôn nhớ về những ngày tháng nơi đây. "
            '"Những nhà vô địch MIS". '
            "Diễn ra từ 02/3 – 28/3/2026. "
            "Đơn vị đảm nhiệm: TPT, Khối VĐNT-TNHT."
        ),
    },
    {
        "title": "Sơ loại Thuyết trình & Hùng biện tiếng Anh Tiểu học – MIS TALKS",
        "date": date(2026, 3, 16),
        "location": "Tại các lớp Tiểu học",
        "description": (
            "Tạo sân chơi cho học sinh Tiểu học giao lưu, học hỏi. "
            "Vòng sơ loại tại lớp, diễn ra từ 16/3 đến 24/4/2026. "
            "Đơn vị đảm nhiệm: BGH, Khối Ngoại Ngữ."
        ),
    },
    {
        "title": "Kỷ niệm ngày Thành lập Đoàn TNCS HCM – Kết nạp Đoàn viên",
        "date": date(2026, 3, 23),
        "time": "07:15",
        "location": "Sân trường MIS",
        "description": (
            "Nêu bật hình ảnh Đoàn TNCS HCM Việt Nam. "
            "Nâng cao nhận thức của HS về vai trò của tổ chức Đoàn (HS THPT). "
            "Kết nạp Đoàn cho HS Khối 10, 11. "
            'Diễn đàn Thanh niên: "Thanh niên MIS với chuyển đổi số và AI", '
            '"Học cùng AI – Thiên tài tỏa sáng". '
            "Đơn vị đảm nhiệm: TPT."
        ),
        "is_featured": True,
    },
    {
        "title": "MIS Innovation Day 2026 – Ngày hội Văn hóa, Thể thao, Khoa học, Sáng tạo & Công nghệ",
        "date": date(2026, 3, 28),
        "location": "Toàn trường MIS",
        "description": (
            "Buổi sáng: Thông qua các hoạt động đa dạng trong ngày để HS trải nghiệm, "
            "thể hiện khả năng, vui chơi, giải trí, sáng tạo, đột phá. "
            "Nằm trong chuỗi hoạt động kỷ niệm 26/3. "
            "Buổi chiều: Chung kết Hội thao 26/3. "
            "Đơn vị đảm nhiệm: TPT, VĐNT-TNHT, GVCN."
        ),
        "is_featured": True,
    },

    # ═══════════════ THÁNG 4/2026 — Con Rồng cháu Tiên ═══════════════
    {
        "title": "Chung kết MIS TALKS – Thuyết trình & Hùng biện tiếng Anh Tiểu học",
        "date": date(2026, 4, 8),
        "location": "Hội trường Grace",
        "description": (
            "Tạo sân chơi cho học sinh Tiểu học giao lưu, học hỏi. "
            "Chung kết tại Hội trường Grace. "
            "Đơn vị đảm nhiệm: BGH, Khối Ngoại Ngữ."
        ),
        "is_featured": True,
    },
    {
        "title": "Ngày hội STEAM Robotic cấp Tiểu học & Thi ứng dụng AI trong học tập",
        "date": date(2026, 4, 15),
        "location": "Toàn trường MIS",
        "description": (
            "Tạo môi trường, sân chơi học tập cho học sinh trau dồi đam mê "
            "với STEAM – Robotic – AI. "
            "Đơn vị đảm nhiệm: BGH, Các Khối Trưởng, Robohub VN."
        ),
    },
    {
        "title": "MIS Dubbing Challenge – Lồng tiếng phim & Video về MIS",
        "date": date(2026, 4, 20),
        "location": "Toàn trường MIS",
        "description": (
            "Sân chơi phát triển ngoại ngữ tiếng Anh, tiếng Trung, tiếng Nhật "
            "giúp HS phát triển toàn diện hơn, học tập liên môn. "
            "Vòng sơ loại: 30/3 – 17/4. Chung kết: 20/4 – 24/4/2026. "
            "Đơn vị đảm nhiệm: Khối Ngoại ngữ, GVCN."
        ),
    },
    {
        "title": "GALA Tác phẩm Văn học Lịch sử lần 2",
        "date": date(2026, 4, 24),
        "location": "Hội trường Grace",
        "description": (
            "Hình thức học tập bằng cảm thụ âm nhạc, thơ ca, phim. "
            "Xây dựng lại các tác phẩm văn học lịch sử trong SGK bằng kịch bản phim. "
            "Sơ loại: 30/3 – 17/4. Chung kết: 24/4/2026. "
            "Đơn vị đảm nhiệm: Tổ KHXH, GVCN, Ban phong trào."
        ),
        "is_featured": True,
    },

    # ═══════════════ THÁNG 5/2026 — Chắp cánh ước mơ ═══════════════
    {
        "title": "K9, K12 dâng hương Đền Hùng – Kết nạp Đoàn",
        "date": date(2026, 5, 8),
        "location": "Đền Hùng, Phú Thọ",
        "description": (
            "Dâng hương các Vua Hùng. Kết nạp Đoàn viên mới. "
            "Đơn vị đảm nhiệm: TPT, Đoàn TNCS HCM."
        ),
    },
    {
        "title": "Lễ Bế giảng Năm học 2025–2026",
        "date": date(2026, 5, 22),
        "location": "Toàn trường MIS",
        "description": (
            "Tổng kết năm học 2025–2026. "
            "Trao giải thưởng, khen thưởng học sinh xuất sắc. "
            "Đơn vị đảm nhiệm: Toàn trường."
        ),
        "is_featured": True,
    },
    {
        "title": "Lễ Trưởng thành & Lễ Ra trường HS Khối 5, 9, 12",
        "date": date(2026, 5, 22),
        "location": "Hội trường Grace",
        "description": (
            "Tri ân thầy cô, cha mẹ. "
            "Lễ trưởng thành cho học sinh khối 5, 9, 12. "
            "Đơn vị đảm nhiệm: TPT, CVP, CMHS, HS K9, K12."
        ),
        "is_featured": True,
    },
    {
        "title": "GALA Tri ân Thầy Cô K9, K12 – Prom Night",
        "date": date(2026, 5, 22),
        "location": "Trường MIS",
        "description": (
            "Chương trình Gala - Prom do chính học sinh K9 - K12 dàn dựng và triển khai vào buổi tối tại trường. "
            "Trang phục dạ hội, giao lưu văn nghệ, ăn tiệc. "
            "PHHS chủ trì, nhà trường hỗ trợ. "
            "Đơn vị đảm nhiệm: TPT, CVP, CMHS, HS K9 và K12."
        ),
        "is_featured": True,
    },
]

created_count = 0
skipped_count = 0

for evt in events_data:
    # Generate slug
    base_slug = slugify(evt["title"])
    if not base_slug:
        base_slug = f"event-{evt['date'].isoformat()}"

    # Check if event already exists (by slug or title+date)
    slug = base_slug
    if Event.objects.filter(slug=slug).exists():
        # Try with date suffix
        slug = f"{base_slug}-{evt['date'].isoformat()}"

    if Event.objects.filter(title=evt["title"], date=evt["date"]).exists():
        skipped_count += 1
        print(f"  SKIP: {evt['title']} ({evt['date']})")
        continue

    time_val = None
    if "time" in evt:
        from datetime import time as time_cls
        h, m = map(int, evt["time"].split(":"))
        time_val = time_cls(h, m)

    event = Event(
        title=evt["title"],
        slug=slug,
        date=evt["date"],
        time=time_val,
        location=evt["location"],
        description=evt["description"],
        is_featured=evt.get("is_featured", False),
    )
    event.save()
    created_count += 1
    print(f"  OK: {evt['title']} ({evt['date']})")

print(f"\nDone! Created: {created_count}, Skipped: {skipped_count}")
