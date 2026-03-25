"""
Cập nhật nội dung chi tiết cho modal 6 card WhyMIS.
Lưu vào field `content` của features section dưới dạng JSON.
Chạy: python scripts/update_whymis_modal_data.py
"""
import json
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

section = page.sections.filter(layout="features").order_by("order").first()
if not section:
    print("ERROR: No features section found!")
    sys.exit(1)

print(f"Updating section: [{section.order}] {section.title}")

DETAILS = [
    {
        "title": "Giáo dục theo học thuyết Đa trí tuệ của Howard Gardner",
        "content": (
            "<p>MIS – Multiple Intelligences School áp dụng <strong>Học thuyết Đa trí tuệ</strong> "
            "(Multiple Intelligences) của Giáo sư Howard Gardner – Đại học Harvard, "
            "một trong những nền tảng giáo dục hiện đại được nhiều quốc gia tiên tiến áp dụng.</p>"
            "<p>Theo học thuyết này, mỗi đứa trẻ đều có những loại trí thông minh khác nhau "
            "và cần được phát triển theo thế mạnh riêng.</p>"
            "<h4>Chương trình học tại MIS giúp học sinh phát triển đa dạng các năng lực:</h4>"
            "<ul>"
            "<li>Trí tuệ ngôn ngữ</li>"
            "<li>Trí tuệ logic – toán học</li>"
            "<li>Trí tuệ âm nhạc</li>"
            "<li>Trí tuệ vận động</li>"
            "<li>Trí tuệ không gian</li>"
            "<li>Trí tuệ giao tiếp</li>"
            "<li>Trí tuệ nội tâm</li>"
            "<li>Trí tuệ thiên nhiên</li>"
            "</ul>"
            "<p>Nhờ đó, mỗi học sinh được khuyến khích khám phá bản thân và phát triển "
            "tiềm năng riêng, thay vì bị giới hạn bởi một khuôn mẫu học tập.</p>"
        ),
    },
    {
        "title": "Phát triển đa ngôn ngữ – nền tảng hội nhập quốc tế",
        "content": (
            "<p>Trong bối cảnh toàn cầu hóa, ngoại ngữ là chìa khóa để học sinh "
            "tiếp cận tri thức và cơ hội trên toàn thế giới.</p>"
            "<p>Tại MIS, học sinh được phát triển đa ngôn ngữ, đặc biệt là:</p>"
            "<ul>"
            "<li><strong>Tiếng Anh</strong> – ngôn ngữ quốc tế</li>"
            "<li><strong>Ngoại ngữ thứ hai</strong> như tiếng Trung</li>"
            "</ul>"
            "<h4>Chương trình ngoại ngữ chú trọng:</h4>"
            "<ul>"
            "<li>Khả năng giao tiếp tự tin</li>"
            "<li>Kỹ năng thuyết trình</li>"
            "<li>Tư duy toàn cầu</li>"
            "</ul>"
            "<p>Điều này giúp học sinh MIS tự tin trở thành những <strong>công dân toàn cầu</strong> "
            "trong tương lai.</p>"
        ),
    },
    {
        "title": "Làm chủ công nghệ với STEAM, Robotics và AI",
        "content": (
            "<p>MIS là một trong những trường <strong>tiên phong</strong> triển khai giáo dục "
            "STEM – STEAM và công nghệ cho học sinh từ sớm.</p>"
            "<h4>Học sinh được tiếp cận với nhiều lĩnh vực hiện đại:</h4>"
            "<ul>"
            "<li>Lập trình</li>"
            "<li>Robotics</li>"
            "<li>Khoa học – Công nghệ</li>"
            "<li>Tư duy thiết kế</li>"
            "<li>Trí tuệ nhân tạo (AI)</li>"
            "</ul>"
            "<h4>Thông qua các dự án thực hành, học sinh phát triển:</h4>"
            "<ul>"
            "<li>Tư duy logic</li>"
            "<li>Khả năng giải quyết vấn đề</li>"
            "<li>Tinh thần sáng tạo</li>"
            "</ul>"
            "<p>Đây là nền tảng quan trọng giúp các em tự tin <strong>làm chủ công nghệ</strong> "
            "trong thế giới tương lai.</p>"
        ),
    },
    {
        "title": "Giá trị sống GRACE và phát triển trí tuệ cảm xúc",
        "content": (
            "<p>Bên cạnh tri thức học thuật, MIS đặc biệt chú trọng giáo dục "
            "<strong>giá trị sống</strong> và <strong>trí tuệ cảm xúc (EQ)</strong>.</p>"
            "<h4>Hệ giá trị GRACE:</h4>"
            "<ul>"
            "<li><strong>G</strong>ratitude – Biết ơn</li>"
            "<li><strong>R</strong>espect – Tôn trọng</li>"
            "<li><strong>A</strong>ccountability – Trách nhiệm</li>"
            "<li><strong>C</strong>ourage – Dũng cảm</li>"
            "<li><strong>E</strong>ngagement – Kết nối</li>"
            "</ul>"
            "<p>Những giá trị này được lồng ghép vào các hoạt động học tập, "
            "trải nghiệm và dự án cộng đồng.</p>"
            "<p>Nhờ đó, học sinh MIS không chỉ học cách thành công, mà còn "
            "học cách <strong>sống tử tế</strong> và có trách nhiệm với xã hội.</p>"
        ),
    },
    {
        "title": "Nghệ thuật và sáng tạo – nuôi dưỡng tâm hồn",
        "content": (
            "<p>MIS tin rằng nghệ thuật là một phần quan trọng trong quá trình "
            "phát triển toàn diện của học sinh.</p>"
            "<h4>Các hoạt động nghệ thuật:</h4>"
            "<ul>"
            "<li>Âm nhạc</li>"
            "<li>Mỹ thuật</li>"
            "<li>Sân khấu</li>"
            "<li>Sáng tạo nghệ thuật</li>"
            "</ul>"
            "<h4>Giúp học sinh:</h4>"
            "<ul>"
            "<li>Phát triển trí tưởng tượng</li>"
            "<li>Thể hiện cảm xúc</li>"
            "<li>Tăng sự tự tin</li>"
            "</ul>"
            "<p>Đồng thời nuôi dưỡng <strong>tư duy sáng tạo</strong> – "
            "một năng lực thiết yếu của thế kỷ 21.</p>"
        ),
    },
    {
        "title": "Môi trường nội trú – rèn luyện tính tự lập",
        "content": (
            "<p>Môi trường nội trú tại MIS được thiết kế nhằm giúp học sinh phát triển:</p>"
            "<ul>"
            "<li>Tính tự lập</li>"
            "<li>Kỹ năng sống</li>"
            "<li>Khả năng quản lý thời gian</li>"
            "<li>Tinh thần trách nhiệm</li>"
            "</ul>"
            "<h4>Trong môi trường nội trú, học sinh học cách:</h4>"
            "<ul>"
            "<li>Chăm sóc bản thân</li>"
            "<li>Sống hòa hợp với cộng đồng</li>"
            "<li>Xây dựng thói quen sinh hoạt khoa học</li>"
            "</ul>"
            "<p>Đây là nền tảng quan trọng giúp các em <strong>trưởng thành</strong> và "
            "sẵn sàng bước vào những môi trường học tập quốc tế trong tương lai.</p>"
        ),
    },
]

section.content = json.dumps(DETAILS, ensure_ascii=False)
section.save()

print(f"  Saved {len(DETAILS)} detail items to section.content")

# Verify
data = json.loads(section.content)
for i, item in enumerate(data):
    print(f"  {i+1}. {item['title'][:60]}")

print("\nDone!")
