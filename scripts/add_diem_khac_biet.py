"""
Script thêm phần "Điểm Khác Biệt – Tại Sao Phụ Huynh Tin Tưởng MIS?" vào trang WhyMIS.
Chèn 6 điểm khác biệt từ Google Doc vào giữa các trụ cột và phần đặc điểm nổi bật.
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

page = AboutPage.objects.filter(page_type="whymis").first()
if not page:
    print("ERROR: WhyMIS page not found!")
    sys.exit(1)

print(f"Found page: {page.title} (id={page.id})")

# ──────────────────────────────────────────────
# 1) Dịch order của các sections hiện có từ order >= 6
#    để tạo khoảng trống cho phần mới (order 6-13)
# ──────────────────────────────────────────────
# Sections hiện tại:
#   0: Hero
#   1: Stats
#   2: Ba Trụ Cột (features)
#   3: Future with AI (text_left)
#   4: Future with Heart (text_right)
#   5: Future with Foreign Languages (text_left)
#   6: Điểm Nổi Bật (features)       → sẽ dời lên order 15
#   7: Quote                          → sẽ dời lên order 16
#   8: CTA                            → sẽ dời lên order 17

# Dời các sections cũ lên trước
sections_to_shift = AboutSection.objects.filter(page=page, order__gte=6).order_by('-order')
for s in sections_to_shift:
    s.order = s.order + 9  # Dời lên 9 bậc (cho chỗ 6-14)
    s.save()
    print(f"  Shifted '{s.title}' to order={s.order}")

# ──────────────────────────────────────────────
# 2) Thêm phần "Điểm Khác Biệt" mới
# ──────────────────────────────────────────────
new_sections = [
    # ── 6. Header section — Giới thiệu tổng quan ──
    {
        "order": 6,
        "layout": "text_right",
        "background": "white",
        "eyebrow": "Điểm Khác Biệt",
        "title": "Tại Sao Phụ Huynh Tin Tưởng MIS?",
        "subtitle": (
            "Trong thời đại công nghệ và trí tuệ nhân tạo phát triển mạnh mẽ, "
            "việc lựa chọn một môi trường giáo dục phù hợp cho con trở thành mối quan tâm lớn của nhiều phụ huynh."
        ),
        "content": (
            "Không chỉ là nơi truyền đạt kiến thức, một ngôi trường tốt cần giúp học sinh "
            "phát triển toàn diện về trí tuệ, cảm xúc, kỹ năng và nhân cách để sẵn sàng bước vào tương lai.\n\n"
            "Tại Trường Phổ thông Liên cấp Đa Trí Tuệ MIS, chương trình giáo dục được xây dựng "
            "dựa trên những triết lý giáo dục tiên tiến, giúp mỗi học sinh phát triển tối đa tiềm năng "
            "của mình. Đây chính là những lý do khiến ngày càng nhiều phụ huynh tin tưởng lựa chọn MIS."
        ),
        "timeline": (
            "Phát triển toàn diện về trí tuệ, cảm xúc, kỹ năng và nhân cách\n"
            "Triết lý giáo dục tiên tiến, phát huy tối đa tiềm năng mỗi học sinh\n"
            "6 điểm khác biệt cốt lõi làm nên thương hiệu MIS"
        ),
    },
    # ── 7. Đa trí tuệ Gardner ──
    {
        "order": 7,
        "layout": "text_left",
        "background": "light",
        "eyebrow": "Điểm Khác Biệt 1",
        "title": "Giáo dục theo Học thuyết Đa Trí Tuệ của Howard Gardner",
        "subtitle": "Mỗi đứa trẻ đều có những loại trí thông minh khác nhau và cần được phát triển theo thế mạnh riêng",
        "content": (
            "MIS áp dụng Học thuyết Đa trí tuệ (Multiple Intelligences) của Giáo sư Howard Gardner – "
            "Đại học Harvard. Theo học thuyết này, mỗi đứa trẻ đều có những loại trí thông minh khác nhau "
            "và cần được phát triển theo thế mạnh riêng.\n\n"
            "Nhờ đó, mỗi học sinh được khuyến khích khám phá bản thân và phát triển tiềm năng riêng, "
            "thay vì bị giới hạn bởi một khuôn mẫu học tập."
        ),
        "timeline": (
            "Trí tuệ ngôn ngữ\n"
            "Trí tuệ logic – toán học\n"
            "Trí tuệ âm nhạc\n"
            "Trí tuệ vận động\n"
            "Trí tuệ không gian\n"
            "Trí tuệ giao tiếp\n"
            "Trí tuệ nội tâm\n"
            "Trí tuệ thiên nhiên"
        ),
    },
    # ── 8. Đa ngôn ngữ ──
    {
        "order": 8,
        "layout": "text_right",
        "background": "white",
        "eyebrow": "Điểm Khác Biệt 2",
        "title": "Phát triển Đa Ngôn Ngữ – Nền Tảng Hội Nhập Quốc Tế",
        "subtitle": "Học sinh MIS tự tin trở thành những công dân toàn cầu trong tương lai",
        "content": (
            "Tại MIS, học sinh được phát triển đa ngôn ngữ, đặc biệt là Tiếng Anh "
            "và ngoại ngữ thứ hai (như tiếng Trung). Chương trình chú trọng khả năng giao tiếp tự tin, "
            "kỹ năng thuyết trình và tư duy toàn cầu.\n\n"
            "Điều này giúp học sinh MIS tự tin trở thành những công dân toàn cầu trong tương lai."
        ),
        "timeline": (
            "Khả năng giao tiếp tự tin bằng đa ngôn ngữ\n"
            "Kỹ năng thuyết trình trước đám đông\n"
            "Tư duy toàn cầu và hiểu biết đa văn hóa"
        ),
    },
    # ── 9. STEAM, Robotics, AI ──
    {
        "order": 9,
        "layout": "text_left",
        "background": "light",
        "eyebrow": "Điểm Khác Biệt 3",
        "title": "Làm Chủ Công Nghệ với STEAM, Robotics và AI",
        "subtitle": "Một trong những trường tiên phong triển khai giáo dục STEAM và công nghệ từ sớm",
        "content": (
            "MIS là một trong những trường tiên phong triển khai giáo dục STEAM và công nghệ từ sớm. "
            "Học sinh được tiếp cận các lĩnh vực hiện đại như Lập trình & Robotics, Khoa học – Công nghệ, "
            "Tư duy thiết kế và Trí tuệ nhân tạo (AI).\n\n"
            "Thông qua các dự án thực hành, học sinh phát triển tư duy logic, "
            "khả năng giải quyết vấn đề và tinh thần sáng tạo."
        ),
        "timeline": (
            "Lập trình & Robotics\n"
            "Khoa học – Công nghệ\n"
            "Tư duy thiết kế\n"
            "Trí tuệ nhân tạo (AI)"
        ),
        "cta_text": "Xem chương trình Robotics",
        "cta_url": "/about/robotics/",
    },
    # ── 10. GRACE & EQ ──
    {
        "order": 10,
        "layout": "text_right",
        "background": "white",
        "eyebrow": "Điểm Khác Biệt 4",
        "title": "Giá Trị Sống GRACE và Phát Triển Trí Tuệ Cảm Xúc (EQ)",
        "subtitle": "Không chỉ học cách thành công mà còn học cách sống tử tế và có trách nhiệm với xã hội",
        "content": (
            "Triết lý giáo dục của nhà trường được xây dựng dựa trên hệ giá trị GRACE:\n\n"
            "• Gratitude – Biết ơn\n"
            "• Respect – Tôn trọng\n"
            "• Accountability – Trách nhiệm\n"
            "• Courage – Dũng cảm\n"
            "• Engagement – Kết nối\n\n"
            "Những giá trị này giúp học sinh MIS không chỉ học cách thành công "
            "mà còn học cách sống tử tế và có trách nhiệm với xã hội."
        ),
        "timeline": (
            "Gratitude – Biết ơn\n"
            "Respect – Tôn trọng\n"
            "Accountability – Trách nhiệm\n"
            "Courage – Dũng cảm\n"
            "Engagement – Kết nối"
        ),
    },
    # ── 11. Nghệ thuật & Sáng tạo ──
    {
        "order": 11,
        "layout": "text_left",
        "background": "light",
        "eyebrow": "Điểm Khác Biệt 5",
        "title": "Nghệ Thuật và Sáng Tạo – Nuôi Dưỡng Tâm Hồn",
        "subtitle": "Tạo điều kiện để học sinh tham gia nhiều hoạt động nghệ thuật",
        "content": (
            "Nhà trường tạo điều kiện để học sinh tham gia nhiều hoạt động nghệ thuật "
            "như Âm nhạc, Mỹ thuật, Sân khấu, giúp các em phát triển trí tưởng tượng, "
            "thể hiện cảm xúc và tăng sự tự tin.\n\n"
            "Nuôi dưỡng tư duy sáng tạo – năng lực thiết yếu của thế kỷ 21."
        ),
        "timeline": (
            "Phát triển trí tưởng tượng\n"
            "Thể hiện cảm xúc và tăng sự tự tin\n"
            "Nuôi dưỡng tư duy sáng tạo – năng lực thiết yếu thế kỷ 21"
        ),
    },
    # ── 12. Môi trường nội trú ──
    {
        "order": 12,
        "layout": "text_right",
        "background": "white",
        "eyebrow": "Điểm Khác Biệt 6",
        "title": "Môi Trường Nội Trú – Rèn Luyện Tính Tự Lập",
        "subtitle": "Giúp học sinh phát triển tính tự lập, kỹ năng sống và tinh thần trách nhiệm",
        "content": (
            "Môi trường nội trú tại MIS được thiết kế nhằm giúp học sinh phát triển "
            "tính tự lập và kỹ năng sống, khả năng quản lý thời gian, "
            "tinh thần trách nhiệm và cách sống hòa hợp với cộng đồng."
        ),
        "timeline": (
            "Tính tự lập và kỹ năng sống\n"
            "Khả năng quản lý thời gian\n"
            "Tinh thần trách nhiệm và sống hòa hợp cộng đồng"
        ),
        "cta_text": "Xem Môi trường nội trú",
        "cta_url": "/about/boarding/",
    },
    # ── 13. Quote kết thúc phần Điểm Khác Biệt ──
    {
        "order": 13,
        "layout": "quote",
        "background": "light",
        "title": "MIS – Nơi mỗi học sinh được phát triển toàn diện",
        "subtitle": "MIS – Educating for the Future, with Heart.",
        "content": (
            "Học là để tự do, sáng tạo – Học để hạnh phúc – Thông minh để hạnh phúc."
        ),
    },
]

created_count = 0
for section_data in new_sections:
    AboutSection.objects.create(page=page, **section_data)
    created_count += 1
    print(f"  Created: [{section_data['order']}] {section_data['title']}")

print(f"\n  Total: Created {created_count} new sections")

# ──────────────────────────────────────────────
# 3) Xác nhận tất cả sections
# ──────────────────────────────────────────────
print("\n--- All WhyMIS Sections ---")
for s in page.sections.all().order_by("order"):
    print(f"  [{s.order:2d}] {s.get_layout_display():24s} | {s.title}")

print(f"\nTotal: {page.sections.count()} sections")
print("Done! Visit /about/whymis/ to see the updated page.")
