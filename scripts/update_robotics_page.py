# -*- coding: utf-8 -*-
"""
Update the Robotics curriculum page content and sections.
Run with: python scripts/update_robotics_page.py
"""
import os
import sys
import django
from pathlib import Path


def render_pdf_page_to_png_bytes(pdf_path: Path, page_index: int, zoom: float = 2.0) -> bytes:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required to render PDF images.") from exc

    with fitz.open(str(pdf_path)) as doc:
        if page_index < 0 or page_index >= doc.page_count:
            raise ValueError(f"PDF page index out of range: {page_index}")
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
        return pix.tobytes("png")


def main() -> None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
    django.setup()

    from about.models import AboutPage, AboutSection
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage

    base_dir = Path(__file__).resolve().parent.parent
    pdf_path = base_dir / "ROBOTICS 2026-2027.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    page, _ = AboutPage.objects.get_or_create(
        page_type="robotics",
        defaults={
            "title": "Chương trình Robotics 2026-2027",
            "content": "",
        },
    )
    page.title = "Chương trình Robotics 2026-2027"
    page.content = ""
    page.save()

    page.sections.all().delete()

    sections = [
        {
            "order": 0,
            "layout": "hero",
            "background": "gradient",
            "eyebrow": "CHƯƠNG TRÌNH CHUYÊN SÂU",
            "title": "Robotics 2026-2027",
            "subtitle": (
                "Học qua trải nghiệm, lắp ráp và lập trình robot; phát triển tư duy "
                "sáng tạo và năng lực công nghệ cho học sinh MIS."
            ),
            "cta_text": "Tư vấn chương trình",
            "cta_url": "/contact/",
            "cta_secondary_text": "Đăng ký tuyển sinh",
            "cta_secondary_url": "/admissions/",
        },
        {
            "order": 1,
            "layout": "full_text",
            "background": "white",
            "eyebrow": "TỔNG QUAN",
            "title": "Đối tác triển khai",
            "content": (
                "ROBOHUB Vietnam là đối tác chính thức cung cấp dịch vụ giáo dục Robotics "
                "cho Trường liên cấp Đa Trí Tuệ - MIS kể từ năm 2019.\n\n"
                "Cùng với sự hỗ trợ của Trường Đại học Sư phạm Hà Nội, ROBOHUB Vietnam "
                "phát triển giáo trình phù hợp, sử dụng thiết bị từ các nhà sản xuất "
                "hàng đầu để học sinh tiếp cận và áp dụng các công nghệ mới nhất."
            ),
        },
        {
            "order": 2,
            "layout": "stats",
            "background": "navy",
            "stat_number": "2019",
            "stat_label": "Hợp tác triển khai Robotics tại MIS",
            "title": "70 phút",
            "subtitle": "Thời lượng mỗi tiết học",
        },
        {
            "order": 3,
            "layout": "full_text",
            "background": "light",
            "eyebrow": "LEARNING BY DOING",
            "title": "Mục tiêu chương trình",
            "content": (
                "- Kích thích tò mò, thỏa sức khám phá, tự do sáng tạo.\n"
                "- Thay đổi tư duy và học theo phương pháp mới.\n"
                "- Đón đầu và áp dụng các công nghệ mới.\n"
                "- Tiếp cận kiến thức về lắp ráp robot, chuyển động cơ học "
                "và vật lý ứng dụng."
            ),
        },
        {
            "order": 4,
            "layout": "full_text",
            "background": "white",
            "eyebrow": "GIÁO DỤC STEAM",
            "title": "Mô hình giảng dạy",
            "content": (
                "STEAM bao gồm: Science - Khoa học, Technology - Công nghệ, "
                "Engineering - Kỹ thuật, Art - Nghệ thuật, Mathematics - Toán học.\n\n"
                "Mô hình lớp học STEAM tập trung vào lắp ráp và lập trình robot.\n\n"
                "Thời lượng: 1 tiết 70 phút.\n"
                "Quy mô lớp: tối đa 30 học sinh, chia thành 5 nhóm.\n"
                "Nhân sự: 1 giáo viên và 5 trợ giảng, mỗi trợ giảng phụ trách 1 nhóm."
            ),
        },
        {
            "order": 5,
            "layout": "full_text",
            "background": "light",
            "eyebrow": "THIẾT BỊ GIẢNG DẠY",
            "title": "Học cụ chuẩn hóa, an toàn",
            "content": (
                "Thiết bị ROBOHUB Vietnam được kiểm định đầy đủ về chất lượng, "
                "độ an toàn cho học sinh và luôn cập nhật những công nghệ tiên tiến.\n\n"
                "Mỗi học sinh có một bộ đồ riêng, kèm sách bài tập và sách lắp ráp."
            ),
        },
        {
            "order": 6,
            "layout": "full_text",
            "background": "white",
            "eyebrow": "CHƯƠNG TRÌNH TIỂU HỌC",
            "title": "8 thử thách khám phá cùng robot",
            "content": (
                "Học sinh tiểu học khám phá cơ chế hoạt động và di chuyển của "
                "các loài động vật, đồng thời làm quen với thao tác lập trình cơ bản.\n\n"
                "8 thử thách tiêu biểu:\n"
                "- Đi thẳng.\n"
                "- Đi lùi và chơi nhạc.\n"
                "- Phát hiện âm thanh.\n"
                "- Đoán số ngẫu nhiên.\n"
                "- Đi theo đường.\n"
                "- Chế độ điều khiển từ xa.\n"
                "- Robot dò đường.\n"
                "- Sử dụng cảm biến."
            ),
        },
        {
            "order": 7,
            "layout": "text_right",
            "background": "light",
            "eyebrow": "HOẠT ĐỘNG NGOẠI KHÓA",
            "title": "CLB - Sự kiện - Giải đấu - Cuộc thi",
            "content": (
                "Học sinh tham gia CLB Robotics, ngày hội trải nghiệm, giải đấu và "
                "các cuộc thi để nâng cao bản lĩnh thi đấu và kỹ năng làm việc nhóm."
            ),
        },
        {
            "order": 8,
            "layout": "cta",
            "background": "accent",
            "title": "Sẵn sàng tham gia chương trình Robotics?",
            "subtitle": "Liên hệ để nhận tư vấn lộ trình phù hợp theo độ tuổi và năng lực.",
            "cta_text": "Đăng ký tư vấn",
            "cta_url": "/contact/",
            "cta_secondary_text": "Xem tuyển sinh",
            "cta_secondary_url": "/admissions/",
        },
    ]

    for data in sections:
        AboutSection.objects.create(page=page, **data)

    sections_by_order = {section.order: section for section in page.sections.all()}
    image_map = {
        0: {"page_index": 0, "filename": "robotics_banner_2026.png"},
        7: {"page_index": 5, "filename": "robotics_activities_2026.png"},
    }

    for order, image_info in image_map.items():
        section = sections_by_order.get(order)
        if not section:
            continue

        png_bytes = render_pdf_page_to_png_bytes(
            pdf_path, image_info["page_index"], zoom=2.0
        )
        if section.image:
            section.image.delete(save=False)

        target_name = image_info["filename"]
        target_path = f"about/sections/{target_name}"
        if default_storage.exists(target_path):
            default_storage.delete(target_path)

        section.image.save(target_name, ContentFile(png_bytes), save=True)

    print(f"Updated Robotics page with {len(sections)} sections.")


if __name__ == "__main__":
    main()
