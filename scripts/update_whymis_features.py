"""
Script cập nhật nội dung 6 card "Điểm Khác Biệt" trong trang WhyMIS.
Cập nhật field `timeline` của section layout='features' chứa 6 card.

Chạy: python scripts/update_whymis_features.py
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

# ─── Tìm trang WhyMIS ───
page = AboutPage.objects.filter(page_type="whymis").first()
if not page:
    print("ERROR: WhyMIS page not found!")
    sys.exit(1)

print(f"Found page: {page.title} (id={page.id})")

# ─── Tìm section features chứa 6 card ───
# Liệt kê tất cả sections để xem
print("\n--- Current WhyMIS Sections ---")
for s in page.sections.all().order_by("order"):
    print(f"  [{s.order:2d}] {s.get_layout_display():24s} | {s.title[:60]}")

# Tìm section features (có thể có nhiều, lấy cái phù hợp)
features_sections = page.sections.filter(layout="features").order_by("order")
print(f"\nFound {features_sections.count()} features section(s)")

# ─── Nội dung mới cho 6 card ───
# Format: "Title | Mô tả ngắn" — mỗi dòng 1 card
# (dùng separator | để template filter `feature_title` / `feature_body` tách đúng)

NEW_TIMELINE = """Giáo Dục Theo Học Thuyết Đa Trí Tuệ | MIS áp dụng Học thuyết Đa trí tuệ của Giáo sư Howard Gardner – Đại học Harvard. Mỗi học sinh được khuyến khích khám phá bản thân và phát triển tiềm năng riêng theo thế mạnh của mình.
Phát Triển Đa Ngôn Ngữ | Tiếng Anh, tiếng Trung với định hướng giao tiếp tự tin, kỹ năng thuyết trình và tư duy toàn cầu – nền tảng hội nhập quốc tế.
Làm Chủ Công Nghệ Với STEAM, Robotics Và AI | Tiên phong triển khai STEAM, Lập trình, Robotics và Trí tuệ nhân tạo. Phát triển tư duy logic, sáng tạo và khả năng giải quyết vấn đề.
Giá Trị Sống GRACE Và Trí Tuệ Cảm Xúc | Biết ơn, Tôn trọng, Trách nhiệm, Dũng cảm, Kết nối – lồng ghép vào học tập, trải nghiệm và dự án cộng đồng.
Nghệ Thuật Và Sáng Tạo | Nuôi dưỡng tâm hồn qua Âm nhạc, Mỹ thuật, Sân khấu. Phát triển trí tưởng tượng và sự tự tin – năng lực thiết yếu thế kỷ 21.
Môi Trường Nội Trú | Rèn luyện tính tự lập, kỹ năng sống và tinh thần trách nhiệm. Học cách chăm sóc bản thân và sống hòa hợp cộng đồng."""

# ─── Nội dung chi tiết cho subtitle của section ───
NEW_SUBTITLE = (
    "Chương trình giáo dục tại MIS được xây dựng trên những triết lý tiên tiến, "
    "giúp mỗi học sinh phát triển toàn diện."
)

# ─── Cập nhật ───
if features_sections.exists():
    # Cập nhật section features ĐẦU TIÊN (card grid chính)
    target_section = features_sections.first()
    print(f"\nUpdating section: [{target_section.order}] {target_section.title}")
    
    old_timeline = target_section.timeline
    target_section.timeline = NEW_TIMELINE.strip()
    if NEW_SUBTITLE:
        target_section.subtitle = NEW_SUBTITLE
    target_section.save()
    
    print(f"  ✅ Updated timeline with 6 items")
    print(f"  ✅ Updated subtitle")
    
    # Xác nhận lại
    target_section.refresh_from_db()
    items = target_section.get_timeline_list()
    print(f"\n--- Updated Items ({len(items)}) ---")
    for i, item in enumerate(items, 1):
        # Simulate template filter
        for sep in (" | ", " – ", " - ", ": "):
            if sep in item:
                title, body = item.split(sep, 1)
                print(f"  {i:02d}. {title.strip()}")
                print(f"      → {body.strip()[:80]}...")
                break
        else:
            print(f"  {i:02d}. {item}")
else:
    print("\n⚠️ No features section found! Creating one...")
    target_section = AboutSection.objects.create(
        page=page,
        order=3,  # Adjust as needed
        layout="features",
        background="light",
        eyebrow="Điểm Khác Biệt",
        title="Những Điểm Khác Biệt Làm Nên MIS",
        subtitle=NEW_SUBTITLE,
        timeline=NEW_TIMELINE.strip(),
    )
    print(f"  ✅ Created new features section at order={target_section.order}")

print("\n✅ Done! Visit /about/whymis/ to see the updated page.")
print("   (Nhấn Ctrl+Shift+R để hard refresh nếu trình duyệt cache)")
