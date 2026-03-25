"""
Script cập nhật nội dung trang "Tại Sao Chọn MIS?" theo Google Doc.
Nội dung bao gồm 3 trụ cột chính: Future with AI, Future with Heart, Future with Foreign Languages.
"""
import os
import sys

import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection

# ──────────────────────────────────────────────
# 1) Cập nhật AboutPage chính
# ──────────────────────────────────────────────
page, created = AboutPage.objects.update_or_create(
    page_type="whymis",
    defaults={
        "title": "Tại Sao Chọn MIS?",
        "content": (
            "Bởi vì tương lai của con không chỉ cần trí tuệ... mà cần cả trái tim. "
            "MIS hướng tới việc xây dựng một ngôi trường nơi học sinh không chỉ giỏi hơn "
            "về học thuật mà còn lớn lên trở thành những con người tự tin, tử tế và hạnh phúc, "
            "biết làm chủ công nghệ và gắn kết với thế giới xung quanh."
        ),
        "image": "about/whymis_mis_competencies.jpeg",
    },
)
action = "Created" if created else "Updated"
print(f"{action} AboutPage: whymis (id={page.id})")

# ──────────────────────────────────────────────
# 2) Xóa sections cũ và tạo mới
# ──────────────────────────────────────────────
old_count = page.sections.count()
page.sections.all().delete()
print(f"  Deleted {old_count} old sections")

sections_data = [
    # ── 0. Hero Section ──
    {
        "order": 0,
        "layout": "hero",
        "background": "gradient",
        "eyebrow": "Tại Sao Chọn MIS",
        "title": "Tại sao chọn MIS?",
        "highlight_text": "Bởi vì tương lai của con không chỉ cần trí tuệ... mà cần cả trái tim",
        "subtitle": (
            "MIS hướng tới việc xây dựng một ngôi trường nơi học sinh không chỉ giỏi hơn "
            "về học thuật mà còn lớn lên trở thành những con người tự tin, tử tế và hạnh phúc, "
            "biết làm chủ công nghệ và gắn kết với thế giới xung quanh."
        ),
        "timeline": (
            "Triết lý giáo dục dựa trên 3 trụ cột: Future with AI – Future with Heart – Future with Foreign Languages\n"
            "Một thế hệ học sinh: Hiểu công nghệ – Hiểu thế giới – Hiểu chính mình"
        ),
        "cta_text": "Đăng ký tư vấn",
        "cta_url": "/tuyen-sinh/",
        "cta_secondary_text": "Đặt lịch tham quan",
        "cta_secondary_url": "/contact/",
    },
    # ── 1. Stats Section ──
    {
        "order": 1,
        "layout": "stats",
        "background": "white",
        "eyebrow": "Thành Tựu",
        "title": "Thành Tựu Nổi Bật",
        "subtitle": (
            "Với sứ mệnh đào tạo những thế hệ người Việt trẻ tự tin, "
            "có đủ trí thức, tài năng và nhân cách, sẵn sàng hội nhập quốc tế."
        ),
        "kpi": (
            "15+ Năm Kinh Nghiệm\n"
            "98% Đậu ĐH Top\n"
            "500+ Học Sinh Mỗi Năm\n"
            "50+ Học Bổng Mỗi Năm\n"
            "3 Trụ Cột Giáo Dục"
        ),
    },
    # ── 2. Features — 3 Trụ Cột ──
    {
        "order": 2,
        "layout": "features",
        "background": "light",
        "eyebrow": "Ba Trụ Cột Giáo Dục",
        "title": "Triết lý Giáo dục MIS",
        "subtitle": (
            "Triết lý giáo dục của MIS được xây dựng trên ba trụ cột, "
            "hướng tới một thế hệ học sinh: Hiểu công nghệ – Hiểu thế giới – Hiểu chính mình."
        ),
        "content": (
            "• FUTURE WITH AI — Khi trẻ không chỉ sử dụng mà làm chủ công nghệ | "
            "Học sinh tiếp cận STEM/STEAM, lập trình và tư duy AI từ sớm. "
            "Không chỉ sử dụng công nghệ mà phải hiểu, làm chủ và ứng dụng để giải quyết vấn đề thực tiễn. "
            "Học tập qua trải nghiệm thực tế (Project-based learning).\n"
            "• FUTURE WITH HEART — Khi giáo dục không chỉ là điểm số, mà là giá trị sống | "
            "Nền tảng giá trị sống GRACE: Gratitude (Biết ơn) – Respect (Tôn trọng) – Accountability (Trách nhiệm) – "
            "Courage (Dũng cảm) – Engagement (Kết nối). "
            "Phát triển trí tuệ cảm xúc (EQ), học cách lắng nghe, thấu hiểu và chia sẻ. "
            "Hoạt động từ thiện thường niên qua Quỹ MIS Charity Foundation (MCF).\n"
            "• FUTURE WITH FOREIGN LANGUAGES — Khi ngôn ngữ là chìa khóa mở cánh cửa thế giới | "
            "Ngoại ngữ không chỉ là môn học mà là công cụ hội nhập và dẫn dắt tương lai. "
            "Tự tin giao tiếp tiếng Anh, tiếng Trung và hiểu biết đa văn hóa. "
            "IELTS 6.0–7.5+, HSK 4–6 khi tốt nghiệp."
        ),
    },
    # ── 3. Future with AI (chi tiết) ──
    {
        "order": 3,
        "layout": "text_left",
        "background": "white",
        "eyebrow": "Trụ cột 1",
        "title": "FUTURE WITH AI",
        "subtitle": "Khi trẻ không chỉ sử dụng mà làm chủ công nghệ",
        "content": (
            "Tại MIS, học sinh được tiếp cận STEM/STEAM, lập trình và tư duy AI từ sớm. "
            "Không chỉ dừng ở việc sử dụng công nghệ, các em được rèn luyện khả năng hiểu, "
            "làm chủ và ứng dụng công nghệ để giải quyết những vấn đề thực tiễn trong cuộc sống.\n\n"
            "Phương pháp Project-based Learning (PBL) giúp học sinh học tập qua trải nghiệm thực tế, "
            "từ đó phát triển tư duy phản biện, sáng tạo và kỹ năng giải quyết vấn đề — "
            "những năng lực cốt lõi cho thế kỷ 21."
        ),
        "timeline": (
            "Tiếp cận STEM/STEAM và tư duy AI từ sớm\n"
            "Lập trình, Robotics và ứng dụng công nghệ\n"
            "Project-based Learning — học qua trải nghiệm\n"
            "Phát triển tư duy phản biện và sáng tạo"
        ),
        "cta_text": "Xem chương trình STEAM",
        "cta_url": "/about/steam/",
    },
    # ── 4. Future with Heart (chi tiết) ──
    {
        "order": 4,
        "layout": "text_right",
        "background": "light",
        "eyebrow": "Trụ cột 2",
        "title": "FUTURE WITH HEART",
        "subtitle": "Khi giáo dục không chỉ là điểm số, mà là giá trị sống",
        "content": (
            "MIS xây dựng nền tảng nhân cách cho học sinh thông qua hệ giá trị GRACE:\n\n"
            "• Gratitude (Biết ơn) — Biết trân trọng những gì mình có\n"
            "• Respect (Tôn trọng) — Tôn trọng bản thân, người khác và môi trường\n"
            "• Accountability (Trách nhiệm) — Chịu trách nhiệm với hành động của mình\n"
            "• Courage (Dũng cảm) — Dám nghĩ, dám làm, dám đối mặt thử thách\n"
            "• Engagement (Kết nối) — Gắn kết với cộng đồng và thế giới\n\n"
            "Phát triển trí tuệ cảm xúc (EQ): học cách lắng nghe, thấu hiểu và chia sẻ. "
            "Hoạt động từ thiện thường niên qua Quỹ MIS Charity Foundation (MCF) giúp các em "
            "hiểu giá trị cho đi và trách nhiệm với cộng đồng."
        ),
        "timeline": (
            "Hệ giá trị sống GRACE\n"
            "Phát triển trí tuệ cảm xúc (EQ)\n"
            "MIS Charity Foundation (MCF)\n"
            "Kỹ năng lắng nghe, thấu hiểu, chia sẻ"
        ),
        "cta_text": "Xem giá trị GRACE",
        "cta_url": "/about/mission/",
    },
    # ── 5. Future with Foreign Languages (chi tiết) ──
    {
        "order": 5,
        "layout": "text_left",
        "background": "white",
        "eyebrow": "Trụ cột 3",
        "title": "FUTURE WITH FOREIGN LANGUAGES",
        "subtitle": "Khi ngôn ngữ là chìa khóa mở cánh cửa thế giới",
        "content": (
            "Tại MIS, ngoại ngữ không chỉ là một môn học — mà là công cụ hội nhập "
            "và dẫn dắt tương lai. Học sinh được đào tạo tự tin giao tiếp, "
            "hiểu biết đa văn hóa và sẵn sàng trở thành công dân toàn cầu.\n\n"
            "Chương trình tiếng Anh chuẩn quốc tế với mục tiêu IELTS 6.0–7.5+ khi tốt nghiệp. "
            "Chương trình tiếng Trung – HSK 4–6, mở rộng cơ hội kết nối với thị trường quốc tế. "
            "Môi trường song ngữ thực hành xuyên suốt từ mầm non đến THPT."
        ),
        "timeline": (
            "IELTS 6.0–7.5+ khi tốt nghiệp\n"
            "HSK 4–6 tiếng Trung\n"
            "Môi trường song ngữ từ Mầm non đến THPT\n"
            "Giao tiếp tự tin, hiểu biết đa văn hóa"
        ),
        "cta_text": "Xem chương trình Tiếng Anh",
        "cta_url": "/about/english/",
    },
    # ── 6. Điểm nổi bật khác ──
    {
        "order": 6,
        "layout": "features",
        "background": "light",
        "eyebrow": "Điểm Nổi Bật",
        "title": "Những Đặc Điểm Làm Nên Sự Khác Biệt",
        "subtitle": (
            "Ngoài 3 trụ cột chính, MIS còn mang đến nhiều giá trị đặc biệt "
            "cho hành trình phát triển toàn diện của mỗi học sinh."
        ),
        "content": (
            "• Phát triển sự tự tin từ rất sớm | "
            "Từ Mầm non, học sinh được khuyến khích thể hiện bản thân qua các hoạt động sáng tạo, "
            "thuyết trình và biểu diễn.\n"
            "• Học tập thông qua trải nghiệm | "
            "Trải nghiệm là người thầy tốt nhất — mỗi bài học đều gắn liền với thực tiễn cuộc sống.\n"
            "• Chú trọng kỹ năng sống | "
            "Kỹ năng xử lý tình huống, giao tiếp, làm việc nhóm và quản lý cảm xúc.\n"
            "• Môi trường giáo dục đầy yêu thương | "
            "Mỗi học sinh là một cá thể duy nhất — được lắng nghe, thấu hiểu và đồng hành."
        ),
    },
    # ── 7. Testimonial ──
    {
        "order": 7,
        "layout": "quote",
        "background": "light",
        "title": "Chị Nguyễn Thị Mai",
        "subtitle": "Phụ huynh học sinh lớp 7",
        "content": (
            "MIS đã thay đổi con tôi hoàn toàn. Con tự tin hơn, năng động hơn "
            "và đặc biệt là yêu việc học. Tôi rất hài lòng với sự phát triển "
            "toàn diện của con tại đây."
        ),
    },
    # ── 8. CTA Section ──
    {
        "order": 8,
        "layout": "cta",
        "background": "gradient",
        "eyebrow": "Bắt đầu ngay",
        "title": "Sẵn Sàng Cho Hành Trình Tuyệt Vời?",
        "subtitle": (
            "Hãy để lại SĐT hoặc đăng ký tham quan trường, trải nghiệm lớp học "
            "và tư vấn lộ trình học tập cá nhân hóa cho con."
        ),
        "cta_text": "Đặt Lịch Tham Quan",
        "cta_url": "/contact/",
        "cta_secondary_text": "Đăng Ký Tuyển Sinh",
        "cta_secondary_url": "/tuyen-sinh/",
    },
]

for section_data in sections_data:
    AboutSection.objects.create(page=page, **section_data)

print(f"  Created {len(sections_data)} new sections")

# ──────────────────────────────────────────────
# 3) Xác nhận
# ──────────────────────────────────────────────
print("\n--- WhyMIS Page Updated ---")
for s in page.sections.all().order_by("order"):
    print(f"  [{s.order}] {s.get_layout_display():20s} | {s.title}")

print("\nDone! Visit /about/whymis/ to see the updated page.")
