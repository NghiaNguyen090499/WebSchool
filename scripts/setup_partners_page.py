"""
Script tạo trang Đối tác chiến lược từ nội dung Google Doc.
Sử dụng hệ thống AboutPage + AboutSection.
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

# ──────────────────────────────────────────────
# 1) Tạo hoặc cập nhật AboutPage
# ──────────────────────────────────────────────
page, created = AboutPage.objects.update_or_create(
    page_type="partners",
    defaults={
        "title": "Đối Tác Chiến Lược",
        "content": (
            "Trường Phổ thông Liên cấp Đa Trí Tuệ MIS tự hào xây dựng mạng lưới hợp tác "
            "với nhiều tổ chức giáo dục, học viện và đơn vị đào tạo hàng đầu trong và ngoài nước. "
            "Thông qua các đối tác chiến lược, MIS mang đến cho học sinh những chương trình học tập "
            "tiên tiến, phương pháp giáo dục hiện đại và cơ hội kết nối với cộng đồng giáo dục quốc tế."
        ),
    },
)
action = "Created" if created else "Updated"
print(f"{action} page: {page.title} (id={page.id})")

# ──────────────────────────────────────────────
# 2) Xóa sections cũ (nếu có) & tạo mới
# ──────────────────────────────────────────────
deleted_count, _ = AboutSection.objects.filter(page=page).delete()
if deleted_count:
    print(f"  Deleted {deleted_count} old sections")

sections = [
    # ── 0. HERO ──
    {
        "order": 0,
        "layout": "hero",
        "background": "gradient",
        "eyebrow": "Đối Tác Chiến Lược",
        "title": "Hợp Tác Cùng Các Tổ Chức Giáo Dục Uy Tín",
        "subtitle": "Mở rộng cơ hội học tập và kết nối toàn cầu cho học sinh MIS",
        "timeline": (
            "Giáo dục STEAM – Robotics – công nghệ và trí tuệ nhân tạo (AI)\n"
            "Các chương trình ngoại ngữ và giao lưu quốc tế\n"
            "Hoạt động phát triển kỹ năng và tư duy sáng tạo\n"
            "Các dự án trải nghiệm thực tế và định hướng nghề nghiệp"
        ),
    },
    # ── 1. STATS ──
    {
        "order": 1,
        "layout": "stats",
        "background": "white",
        "eyebrow": "Con Số Ấn Tượng",
        "title": "Mạng Lưới Đối Tác Giáo Dục",
        "subtitle": (
            "MIS hợp tác với nhiều tổ chức giáo dục và đơn vị đào tạo uy tín "
            "nhằm mang đến cho học sinh những chương trình học tập chất lượng "
            "và cơ hội phát triển toàn diện."
        ),
        "kpi": (
            "4 Nhóm Đối Tác\n"
            "10+ Tổ Chức Giáo Dục\n"
            "6 Chương Trình Hợp Tác\n"
            "15+ Năm Đồng Hành"
        ),
    },
    # ── 2. PARTNER CATEGORIES (Feature Grid) ──
    {
        "order": 2,
        "layout": "features",
        "background": "light",
        "eyebrow": "Mạng Lưới Đối Tác",
        "title": "4 Nhóm Đối Tác Chiến Lược",
        "subtitle": (
            "MIS hợp tác với nhiều tổ chức giáo dục và đơn vị đào tạo uy tín "
            "nhằm mang đến cho học sinh cơ hội phát triển toàn diện."
        ),
        "content": (
            "• Công Nghệ & STEAM | Robotics, lập trình, tư duy thiết kế và sáng tạo công nghệ\n"
            "• Ngoại Ngữ & Hội Nhập | Tiếng Anh học thuật, tiếng Trung và giao lưu quốc tế\n"
            "• Giáo Dục & Phát Triển | Trí tuệ cảm xúc, giá trị sống GRACE và kỹ năng lãnh đạo\n"
            "• Cộng Đồng & Trải Nghiệm | Thiện nguyện, giáo dục giá trị sống và dự án cộng đồng"
        ),
    },
    # ── 3. NHÓM 1: Công nghệ & STEAM ──
    {
        "order": 3,
        "layout": "text_left",
        "background": "white",
        "eyebrow": "Nhóm Đối Tác 1",
        "title": "Đối Tác Giáo Dục Công Nghệ và STEAM",
        "subtitle": "Tiên phong triển khai giáo dục STEAM, Robotics và công nghệ sáng tạo",
        "content": (
            "Các đối tác giáo dục STEM – STEAM giúp học sinh tiếp cận khoa học, "
            "công nghệ, kỹ thuật và sáng tạo từ sớm. Thông qua các chương trình hợp tác, "
            "học sinh MIS được trải nghiệm thực hành, phát triển tư duy logic "
            "và khả năng giải quyết vấn đề."
        ),
        "timeline": (
            "Robohub Vietnam — Chương trình Robotics và công nghệ sáng tạo cho Tiểu học\n"
            "MathExpress — Phát triển tư duy toán học theo phương pháp Singapore\n"
            "Học viện STEM — Chương trình lập trình và công nghệ cho toàn trường\n"
            "Đối tác STEM-STEAM — Tiếp cận khoa học, công nghệ từ sớm"
        ),
        "cta_text": "Xem chương trình Robotics",
        "cta_url": "/about/curriculum/robotics/",
    },
    # ── 4. NHÓM 2: Ngoại ngữ ──
    {
        "order": 4,
        "layout": "text_right",
        "background": "light",
        "eyebrow": "Nhóm Đối Tác 2",
        "title": "Đối Tác Đào Tạo Ngoại Ngữ",
        "subtitle": "Phát triển đa ngôn ngữ, nền tảng hội nhập quốc tế",
        "content": (
            "Các đơn vị đào tạo ngoại ngữ và giao lưu quốc tế giúp học sinh MIS "
            "phát triển khả năng hội nhập toàn cầu. Chương trình chú trọng khả năng "
            "giao tiếp tự tin, kỹ năng thuyết trình và tư duy toàn cầu."
        ),
        "timeline": (
            "Jaxtina English Center — Đào tạo tiếng Anh học thuật và giao tiếp quốc tế\n"
            "Tiếng Trung Quốc Tế Thời Đại — Đào tạo tiếng Trung và du học Trung Quốc\n"
            "Giao lưu quốc tế — Kết nối với các trường đối tác trên thế giới"
        ),
        "cta_text": "Xem chương trình Ngoại ngữ",
        "cta_url": "/about/curriculum/english/",
    },
    # ── 5. NHÓM 3: Giáo dục & phát triển ──
    {
        "order": 5,
        "layout": "text_left",
        "background": "white",
        "eyebrow": "Nhóm Đối Tác 3",
        "title": "Đối Tác Giáo Dục và Phát Triển Học Sinh",
        "subtitle": "Trí tuệ cảm xúc, giá trị sống và kỹ năng lãnh đạo tương lai",
        "content": (
            "Các tổ chức giáo dục và chuyên gia đào tạo kỹ năng giúp học sinh phát triển "
            "tư duy sáng tạo, kỹ năng lãnh đạo, khả năng giao tiếp và hợp tác, "
            "cùng với định hướng nghề nghiệp tương lai."
        ),
        "timeline": (
            "Seroto Foundation — Chương trình giáo dục trí tuệ cảm xúc\n"
            "Lyceum Global — Chương trình Giá trị sống và cảm xúc xã hội GRACE\n"
            "Tư duy sáng tạo và kỹ năng lãnh đạo\n"
            "Định hướng nghề nghiệp tương lai"
        ),
        "cta_text": "Xem chương trình Kỹ năng sống",
        "cta_url": "/about/curriculum/lifeskills/",
    },
    # ── 6. NHÓM 4: Cộng đồng & trải nghiệm ──
    {
        "order": 6,
        "layout": "text_right",
        "background": "light",
        "eyebrow": "Nhóm Đối Tác 4",
        "title": "Đối Tác Cộng Đồng và Giáo Dục Trải Nghiệm",
        "subtitle": "Phát triển tư duy nhân văn và trách nhiệm với xã hội",
        "content": (
            "Bên cạnh các tổ chức giáo dục, MIS còn hợp tác với nhiều tổ chức cộng đồng "
            "và quỹ xã hội nhằm triển khai các chương trình giáo dục giá trị sống, "
            "hoạt động thiện nguyện và trách nhiệm xã hội.\n\n"
            "Những hoạt động này giúp học sinh MIS không chỉ học tập trong lớp học "
            "mà còn phát triển tư duy nhân văn và trách nhiệm với xã hội."
        ),
        "timeline": (
            "Giáo dục giá trị sống\n"
            "Hoạt động thiện nguyện và trách nhiệm xã hội\n"
            "Các dự án học tập cộng đồng\n"
            "Chương trình trải nghiệm thực tế cho học sinh"
        ),
        "cta_text": "Xem Trách nhiệm xã hội",
        "cta_url": "/trach-nhiem-xa-hoi/",
    },
    # ── 7. QUOTE ──
    {
        "order": 7,
        "layout": "quote",
        "background": "white",
        "title": "MIS – Kết Nối Tri Thức, Mở Rộng Tương Lai",
        "subtitle": "MIS – Educating for the Future, with Heart.",
        "content": (
            "Thông qua mạng lưới hợp tác giáo dục uy tín, MIS mang đến cho học sinh "
            "một môi trường học tập hiện đại, nơi các em được tiếp cận với những chương trình "
            "giáo dục tiên tiến và cơ hội phát triển toàn diện."
        ),
    },
    # ── 8. FEATURES: Giá trị hợp tác ──
    {
        "order": 8,
        "layout": "features",
        "background": "light",
        "eyebrow": "Giá Trị Hợp Tác",
        "title": "Lợi Ích Khi Hợp Tác Cùng MIS",
        "subtitle": (
            "Với định hướng Future with AI – Future with Heart – Future with Foreign Languages, "
            "MIS không ngừng mở rộng hợp tác với các tổ chức giáo dục."
        ),
        "content": (
            "• Nâng Cao Chất Lượng Đào Tạo | Tiếp cận chương trình giáo dục tiên tiến từ đối tác chuyên nghiệp\n"
            "• Cơ Hội Phát Triển Toàn Diện | Phát triển tri thức, kỹ năng và khả năng hội nhập toàn cầu\n"
            "• Kết Nối Quốc Tế | Giao lưu, trao đổi với các trường đối tác trên thế giới\n"
            "• Chuẩn Bị Tương Lai | Trang bị cho học sinh những năng lực cần thiết cho thế kỷ 21"
        ),
    },
    # ── 9. CTA ──
    {
        "order": 9,
        "layout": "cta",
        "background": "gradient",
        "eyebrow": "Liên Hệ Hợp Tác",
        "title": "Trở Thành Đối Tác Của MIS",
        "subtitle": (
            "MIS luôn chào đón các tổ chức giáo dục, doanh nghiệp và đơn vị đào tạo "
            "cùng hợp tác xây dựng cộng đồng giáo dục tiên tiến."
        ),
        "cta_text": "Liên Hệ Hợp Tác",
        "cta_url": "/lien-he/",
    },
]

created_count = 0
for section_data in sections:
    AboutSection.objects.create(page=page, **section_data)
    created_count += 1
    print(f"  Created: [{section_data['order']}] {section_data['layout']:12s} | {section_data['title']}")

print(f"\nTotal: {created_count} sections created")
print(f"Visit /about/partners/ to see the page.")
