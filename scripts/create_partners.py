"""
Script tạo các Partner entries cho trang Đối tác chiến lược.
Logo upload qua Django Admin sau.
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from core.models import Partner

partners_data = [
    # ── Nhóm 1: Công nghệ & STEAM ──
    {
        "name": "Robohub Vietnam",
        "partner_type": "technology",
        "description": "Chương trình Robotics và công nghệ sáng tạo cho Tiểu học – THCS",
        "url": "",
        "order": 1,
        "show_in_marquee": True,
    },
    {
        "name": "MathExpress",
        "partner_type": "technology",
        "description": "Phát triển tư duy toán học theo phương pháp Singapore",
        "url": "",
        "order": 2,
        "show_in_marquee": True,
    },
    {
        "name": "Học viện STEM",
        "partner_type": "technology",
        "description": "Chương trình lập trình và công nghệ sáng tạo cho toàn trường",
        "url": "",
        "order": 3,
        "show_in_marquee": True,
    },
    # ── Nhóm 2: Ngoại ngữ ──
    {
        "name": "Jaxtina English Center",
        "partner_type": "language",
        "description": "Đào tạo tiếng Anh học thuật và giao tiếp quốc tế",
        "url": "https://jaxtina.com",
        "order": 4,
        "show_in_marquee": True,
    },
    {
        "name": "Tiếng Trung Quốc Tế Thời Đại",
        "partner_type": "language",
        "description": "Đào tạo tiếng Trung và hỗ trợ du học Trung Quốc",
        "url": "",
        "order": 5,
        "show_in_marquee": True,
    },
    # ── Nhóm 3: Giáo dục & Phát triển ──
    {
        "name": "Seroto Foundation",
        "partner_type": "education",
        "description": "Chương trình giáo dục trí tuệ cảm xúc (EQ)",
        "url": "",
        "order": 6,
        "show_in_marquee": True,
    },
    {
        "name": "Lyceum Global",
        "partner_type": "education",
        "description": "Chương trình Giá trị sống và cảm xúc xã hội GRACE",
        "url": "",
        "order": 7,
        "show_in_marquee": True,
    },
    # ── Nhóm 4: Cộng đồng ──
    {
        "name": "MIS Community Partners",
        "partner_type": "community",
        "description": "Giáo dục giá trị sống, hoạt động thiện nguyện và trách nhiệm xã hội",
        "url": "",
        "order": 8,
        "show_in_marquee": False,
    },
]

created_count = 0
updated_count = 0
for data in partners_data:
    partner, created = Partner.objects.update_or_create(
        name=data["name"],
        defaults=data,
    )
    if created:
        created_count += 1
        print(f"  ✅ Created: {partner.name} ({partner.get_partner_type_display()})")
    else:
        updated_count += 1
        print(f"  🔄 Updated: {partner.name} ({partner.get_partner_type_display()})")

print(f"\nTotal: {created_count} created, {updated_count} updated")
print(f"Upload logos via Django Admin: /admin/core/partner/")
