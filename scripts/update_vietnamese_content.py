# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")
django.setup()

from about.models import AboutPage, AboutSection  # noqa: E402
from admissions.models import AdmissionInfo  # noqa: E402
from core.models import Campus, CoreValue, SchoolInfo, StudentLifePage, WebsiteGoal  # noqa: E402


def update_school_info():
    school_info = SchoolInfo.get_active() or SchoolInfo.objects.first()
    if not school_info:
        school_info = SchoolInfo.objects.create(
            name_vn="Hệ thống Giáo dục Đa Trí Tuệ – MIS",
            name_en="Multiple Intelligences School System (MIS)",
            short_name="MIS",
            address="[ĐIỀN SAU]",
            hotline="[ĐIỀN SAU]",
            admissions_email="[ĐIỀN SAU]",
            is_active=True,
        )

    school_info.name_vn = "Hệ thống Giáo dục Đa Trí Tuệ – MIS"
    school_info.name_en = "Multiple Intelligences School System (MIS)"
    if not school_info.short_name:
        school_info.short_name = "MIS"
    if not school_info.short_description:
        school_info.short_description = (
            "Đa Trí Tuệ – Một Nhân Cách. MIS kiến tạo môi trường học tập khai phóng "
            "để mỗi học sinh phát triển trí tuệ, cảm xúc và nhân cách toàn diện."
        )
    school_info.save()

    return school_info


def update_campuses(school_info):
    primary = Campus.objects.filter(school=school_info, is_primary=True).first()
    if primary:
        primary.name = "Campus chính – Cầu Giấy"
        if not primary.address:
            primary.address = school_info.address
        if not primary.phone:
            primary.phone = school_info.hotline or ""
        if not primary.email:
            primary.email = school_info.admissions_email or ""
        primary.is_active = True
        primary.order = 1
        primary.save()
    else:
        Campus.objects.create(
            school=school_info,
            name="Campus chính – Cầu Giấy",
            address=school_info.address,
            phone=school_info.hotline or "",
            email=school_info.admissions_email or "",
            is_primary=True,
            is_active=True,
            order=1,
        )

    secondary = Campus.objects.filter(school=school_info, is_primary=False).first()
    if secondary:
        secondary.name = "MIS Pandora Landscape – Láng – Hòa Lạc"
        if not secondary.address:
            secondary.address = "MIS Pandora Landscape – khu vực Láng – Hòa Lạc, Hà Nội"
        secondary.is_active = True
        secondary.order = 2
        secondary.save()
    else:
        Campus.objects.create(
            school=school_info,
            name="MIS Pandora Landscape – Láng – Hòa Lạc",
            address="MIS Pandora Landscape – khu vực Láng – Hòa Lạc, Hà Nội",
            is_primary=False,
            is_active=True,
            order=2,
        )


def update_website_goals():
    WebsiteGoal.objects.all().delete()
    WebsiteGoal.objects.create(
        goal_type="tuyen_sinh",
        description="Tăng chuyển đổi đăng ký tư vấn, tham quan và nhập học bằng thông tin rõ ràng, đáng tin cậy.",
        priority=4,
        is_active=True,
    )
    WebsiteGoal.objects.create(
        goal_type="truyen_thong",
        description="Xây dựng hình ảnh thương hiệu giáo dục cao cấp, nhân văn và tiên phong đổi mới.",
        priority=3,
        is_active=True,
    )
    WebsiteGoal.objects.create(
        goal_type="ket_noi",
        description="Cung cấp thông tin đầy đủ cho phụ huynh, tăng cường kết nối Nhà trường – Gia đình – Học sinh.",
        priority=2,
        is_active=True,
    )
    WebsiteGoal.objects.create(
        goal_type="tin_tuc",
        description="Truyền thông hoạt động, sự kiện và thành tựu nổi bật của MIS.",
        priority=1,
        is_active=True,
    )


def update_student_life():
    student_life_content = (
        "Đời sống học sinh tại MIS là sự hòa quyện giữa học tập khai phóng và trải nghiệm thực tiễn. "
        "Mỗi ngày đến trường, học sinh được khám phá, thử thách bản thân và kết nối trong một cộng đồng nhân văn.\n\n"
        "Nhà trường khuyến khích các em phát triển năng lực 5Cs, nuôi dưỡng cảm xúc lành mạnh và xây dựng lối sống tích cực, "
        "để trưởng thành với một nhân cách vững vàng và tinh thần học tập suốt đời."
    )

    StudentLifePage.objects.update_or_create(
        slug="doi-song-hoc-sinh",
        defaults={
            "title": "Đời sống học sinh",
            "description": "Không gian học tập giàu trải nghiệm, nơi mỗi ngày đến trường là một ngày khám phá và kết nối.",
            "content": student_life_content,
            "activities": "\n".join(
                [
                    "STEAM & Robotics",
                    "Nghệ thuật biểu diễn và mỹ thuật",
                    "Thể thao và rèn luyện thể chất",
                    "Ngoại khóa – dã ngoại – trại kỹ năng",
                    "Dự án cộng đồng và thiện nguyện",
                    "Hoạt động kết nối gia đình – nhà trường",
                ]
            ),
            "clubs": "\n".join(
                [
                    "CLB Robotics",
                    "CLB Nghệ thuật",
                    "CLB Bóng đá",
                    "CLB Debate",
                    "CLB Toán ứng dụng",
                    "CLB Khoa học",
                    "CLB Âm nhạc",
                    "CLB Mỹ thuật",
                ]
            ),
            "events": (
                "Các sự kiện thường niên: Open Day, Science Fair, MIS Cup, Festival Nghệ thuật, Ngày hội Gia đình.\n"
                "Ngoài ra còn có các talkshow kỹ năng, hoạt động hướng nghiệp và chương trình trải nghiệm ngoài lớp học."
            ),
            "facilities": (
                "Không gian học tập xanh, an toàn với phòng học thông minh, phòng lab STEAM, thư viện mở, "
                "khu thể thao đa năng và khu trải nghiệm thiên nhiên tại MIS Pandora Landscape."
            ),
            "is_active": True,
            "order": 1,
        },
    )


def update_core_values():
    CoreValue.objects.all().delete()
    core_values = [
        (
            "Gratitude | Biết ơn",
            "Trân trọng những điều tốt đẹp, biết ơn gia đình, thầy cô và cộng đồng.",
            "fas fa-heart",
            1,
        ),
        (
            "Respect | Tôn trọng",
            "Tôn trọng bản thân, người khác và sự khác biệt.",
            "fas fa-handshake",
            2,
        ),
        (
            "Accountability | Trách nhiệm",
            "Chủ động, kỷ luật và chịu trách nhiệm với lựa chọn của mình.",
            "fas fa-clipboard-check",
            3,
        ),
        (
            "Courage | Can đảm",
            "Dám thử thách, vượt qua giới hạn và kiên định theo đuổi mục tiêu.",
            "fas fa-shield-alt",
            4,
        ),
        (
            "Engagement | Dấn thân & Nối kết",
            "Tích cực tham gia, biết sẻ chia và kết nối để cùng phát triển.",
            "fas fa-link",
            5,
        ),
    ]
    for title, description, icon, order in core_values:
        CoreValue.objects.create(
            title=title,
            description=description,
            icon=icon,
            order=order,
        )


def update_about_pages():
    page, _ = AboutPage.objects.get_or_create(
        page_type="mission", defaults={"title": "Về chúng tôi", "content": ""}
    )
    page.title = "Về chúng tôi"
    page.content = ""
    page.save()

    page.sections.all().delete()

    hero_subtitle = (
        "Đa Trí Tuệ – Một Nhân Cách. MIS kiến tạo môi trường giáo dục khai phóng, "
        "nuôi dưỡng trí tuệ – cảm xúc – nhân cách, sẵn sàng hội nhập."
    )

    mission_content = (
        "VỚI HỌC SINH\n"
        "Khơi dậy tiềm năng cá nhân, phát triển trí tuệ – cảm xúc – thể chất hài hòa, "
        "sẵn sàng trở thành công dân toàn cầu và người kiến tạo tương lai.\n\n"
        "VỚI GIÁO VIÊN\n"
        "Xây dựng môi trường giáo dục hiện đại, tôn trọng sáng tạo, trách nhiệm, nâng cao năng lực chuyên môn; "
        "hướng tới mỗi giáo viên là nhà sư phạm đích thực – người dẫn dắt – nhà tổ chức – nhà tâm lý có tâm sáng.\n\n"
        "VỚI XÃ HỘI\n"
        "Góp phần xây dựng hệ sinh thái giáo dục thông minh – xanh – sáng tạo, vì một Việt Nam hạnh phúc và phát triển bền vững."
    )

    vision_content = (
        "Trở thành một trong những trường tiên phong về chất lượng giáo dục, đổi mới và bền vững tại Việt Nam, MIS hướng tới:\n\n"
        "PHÁT TRIỂN HỆ SINH THÁI GIÁO DỤC BỀN VỮNG\n"
        "Xây dựng mô hình giáo dục toàn diện, thích ứng với thay đổi toàn cầu.\n\n"
        "TẠO RA MỘT CỘNG ĐỒNG GẮN KẾT MẠNH MẼ\n"
        "Kết nối chặt chẽ gia đình – nhà trường – học sinh để phát huy tối đa tiềm năng về tri thức, kỹ năng và nhân cách, "
        "trở thành công dân có trách nhiệm và đóng góp tích cực cho xã hội.\n\n"
        "ĐÀO TẠO NHÀ LÃNH ĐẠO TƯƠNG LAI\n"
        "Truyền cảm hứng để học sinh trở thành những nhà lãnh đạo hạnh phúc, những nhà đổi mới có tư duy phản biện và sáng tạo, "
        "sẵn sàng đối mặt với thách thức toàn cầu và góp phần vào sự phát triển bền vững của xã hội và thế giới."
    )

    sections = [
        {
            "order": 0,
            "layout": "hero",
            "background": "navy",
            "eyebrow": "HỆ THỐNG GIÁO DỤC ĐA TRÍ TUỆ – MIS",
            "title": "VỀ CHÚNG TÔI",
            "subtitle": hero_subtitle,
        },
        {
            "order": 1,
            "layout": "text_left",
            "background": "white",
            "eyebrow": "SỨ MỆNH",
            "title": "Sứ mệnh của MIS",
            "content": mission_content,
        },
        {
            "order": 2,
            "layout": "text_right",
            "background": "light",
            "eyebrow": "TẦM NHÌN",
            "title": "Tầm nhìn của MIS",
            "content": vision_content,
        },
    ]

    for data in sections:
        AboutSection.objects.create(page=page, **data)

    vision_page, _ = AboutPage.objects.get_or_create(page_type="vision")
    vision_page.title = "Tầm nhìn của MIS"
    vision_page.content = vision_content
    vision_page.save()

    english_page, _ = AboutPage.objects.get_or_create(page_type="overview_english")
    english_page.title = "Hệ Tiếng Anh Tài Năng"
    english_page.content = ""
    english_page.save()


def update_admissions():
    process = (
        "1) Đăng ký tư vấn và nhận thông tin.\n"
        "2) Tư vấn trực tiếp/online và tham quan campus.\n"
        "3) Đánh giá đầu vào (nếu cần theo cấp học).\n"
        "4) Thông báo kết quả và tư vấn lộ trình học tập.\n"
        "5) Hoàn tất hồ sơ nhập học và tài chính.\n"
        "6) Đón tiếp định hướng trước khi nhập học."
    )

    tuition_info = (
        "Học phí và chính sách ưu đãi được tư vấn theo từng đợt tuyển sinh. "
        "Vui lòng liên hệ để nhận bảng học phí chi tiết."
    )

    benefits = (
        "Thông tin học bổng/ưu đãi được cập nhật theo từng thời điểm. "
        "Vui lòng liên hệ để được tư vấn."
    )

    requirements_common = (
        "• Học sinh trong độ tuổi/khối lớp phù hợp.\n"
        "• Hồ sơ nhập học theo quy định của nhà trường.\n"
        "• Tham gia đánh giá đầu vào (nếu cần theo cấp học)."
    )

    admissions_updates = {
        "mam_non": {
            "age_range": "3–6 tuổi",
            "description": (
                "Chương trình Mầm non MIS phát triển toàn diện “Thể chất – Trí tuệ – Cảm xúc”, "
                "nuôi dưỡng nền tảng an toàn cảm xúc và thói quen học tập tích cực cho trẻ trước khi vào Lớp 1."
            ),
            "curriculum": (
                "• Hands-on learning qua trải nghiệm đa giác quan.\n"
                "• Phát triển ngôn ngữ, tư duy logic, kỹ năng xã hội và cảm xúc.\n"
                "• Song ngữ 50% Tiếng Anh – 50% Tiếng Việt."
            ),
        },
        "tieu_hoc": {
            "age_range": "Lớp 1–5",
            "description": (
                "Chương trình Tiểu học bám sát Bộ GD&ĐT, tích hợp STEM/STEAM và dự án liên môn, "
                "tập trung khơi mở đa trí tuệ và định hình nhân cách."
            ),
            "curriculum": (
                "• Tiếng Anh theo chuẩn Cambridge, rèn tư duy phản biện và năng lực số.\n"
                "• Dự án học tập cá nhân hóa theo năng lực.\n"
                "• Làm quen ngoại ngữ 2: Tiếng Trung."
            ),
        },
        "thcs": {
            "age_range": "Lớp 6–9",
            "description": (
                "Chương trình THCS định hình tư duy toàn diện, phát triển kỹ năng sống và năng lực cảm xúc xã hội, "
                "đẩy mạnh nghiên cứu khoa học và trải nghiệm thực tế."
            ),
            "curriculum": (
                "• Song ngữ Anh – Việt, chuẩn đầu ra Cambridge; luyện IELTS từ lớp 6.\n"
                "• STEAM và học qua trải nghiệm, phát triển 8 loại hình trí thông minh.\n"
                "• CLB chuyên sâu: Robotics, Toán ứng dụng, Debate, Thiết kế AI."
            ),
        },
        "thpt": {
            "age_range": "Lớp 10–12",
            "description": (
                "Chương trình THPT đa lộ trình, kết hợp Bộ GD&ĐT với các môn tự chọn và định hướng nghề nghiệp cá nhân hóa, "
                "giúp học sinh sẵn sàng cho đại học hoặc du học."
            ),
            "curriculum": (
                "• Lộ trình Công nghệ Quốc tế (liên kết Aptech) hoặc HSK5+ (Trung Quốc).\n"
                "• Tài năng Toán học & Tài năng Tiếng Anh.\n"
                "• Hướng nghiệp 4.0: thực tập doanh nghiệp, chuẩn bị chứng chỉ quốc tế."
            ),
        },
    }

    for level, data in admissions_updates.items():
        admission = AdmissionInfo.objects.filter(level=level).first()
        if not admission:
            admission = AdmissionInfo.objects.create(
                level=level,
                title=f"Tuyển sinh {level}",
                description=data["description"],
                requirements=requirements_common,
                tuition_info=tuition_info,
                process=process,
            )
        admission.age_range = data["age_range"]
        admission.description = data["description"]
        admission.curriculum = data["curriculum"]
        admission.requirements = requirements_common
        admission.tuition_info = tuition_info
        admission.process = process
        admission.benefits = benefits
        admission.save()


def main():
    school_info = update_school_info()
    update_campuses(school_info)
    update_website_goals()
    update_student_life()
    update_core_values()
    update_about_pages()
    update_admissions()


if __name__ == "__main__":
    main()
