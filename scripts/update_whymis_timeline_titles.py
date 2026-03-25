"""Cập nhật timeline chỉ chứa tiêu đề thuần túy (bỏ body text)."""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

page = AboutPage.objects.filter(page_type="whymis").first()
section = page.sections.filter(layout="features").order_by("order").first()

NEW_TIMELINE = """Giáo dục theo học thuyết Đa trí tuệ của Howard Gardner
Phát triển đa ngôn ngữ – nền tảng hội nhập quốc tế
Làm chủ công nghệ với STEAM, Robotics và AI
Giá trị sống GRACE và phát triển trí tuệ cảm xúc
Nghệ thuật và sáng tạo – nuôi dưỡng tâm hồn
Môi trường nội trú – rèn luyện tính tự lập"""

section.timeline = NEW_TIMELINE.strip()
section.save()

items = section.get_timeline_list()
print(f"Updated {len(items)} items:")
for i, t in enumerate(items, 1):
    print(f"  {i:02d}. {t}")
print("Done!")
