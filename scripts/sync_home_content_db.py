from pathlib import Path

from django.core.files import File

from core.models import Achievement, FounderMessage, ParentTestimonial, Pillar


def upsert_achievements():
    records = [
        {
            "title": "Đầu ra ngoại ngữ",
            "stat_value": "50%",
            "stat_label": "Học sinh K12 đạt IELTS 5.0-7.5 & HSK 3-6",
            "description": "Thống kê đầu ra ngoại ngữ theo brochure 2026-2027.",
            "icon": "fas fa-language",
            "tags": "IELTS, HSK",
            "category": "language",
            "color": "blue",
            "is_stat": True,
            "is_card": False,
            "order": 1,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "Học bổng du học",
            "stat_value": "15",
            "stat_label": "Học sinh đạt học bổng du học cao tại các quốc gia phát triển",
            "description": "Số lượng học sinh có học bổng du học.",
            "icon": "fas fa-graduation-cap",
            "tags": "Scholarship",
            "category": "scholarship",
            "color": "green",
            "is_stat": True,
            "is_card": False,
            "order": 2,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "Đại học hàng đầu",
            "stat_value": "98%",
            "stat_label": "Học sinh K12 đỗ vào các trường Đại học hàng đầu Việt Nam",
            "description": "Tỷ lệ đỗ đại học top theo hồ sơ tuyển sinh.",
            "icon": "fas fa-university",
            "tags": "University",
            "category": "academic",
            "color": "red",
            "is_stat": True,
            "is_card": False,
            "order": 3,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "TOP 10",
            "stat_value": "",
            "stat_label": "",
            "description": "Thương hiệu tiêu biểu Châu Á - Thái Bình Dương 2025 (Trung Quốc)",
            "icon": "fas fa-award",
            "tags": "Brand Award 2025",
            "category": "competition",
            "color": "red",
            "is_stat": False,
            "is_card": True,
            "order": 10,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "TOP 50",
            "stat_value": "",
            "stat_label": "",
            "description": "Thương hiệu nổi tiếng ASEAN 2025 (Singapore)",
            "icon": "fas fa-globe-asia",
            "tags": "Brand Award 2025",
            "category": "competition",
            "color": "amber",
            "is_stat": False,
            "is_card": True,
            "order": 11,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "TOP 20",
            "stat_value": "",
            "stat_label": "",
            "description": "Thương hiệu sản phẩm dịch vụ chất lượng vàng vì quyền lợi người tiêu dùng Việt Nam 2025",
            "icon": "fas fa-medal",
            "tags": "Brand Award 2025",
            "category": "competition",
            "color": "red",
            "is_stat": False,
            "is_card": True,
            "order": 12,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "ASMO Quốc tế - Indonesia",
            "stat_value": "",
            "stat_label": "",
            "description": "Vòng 1: 2 giải Bạc - 1 giải Đồng. Vòng 2: 2 giải Vàng - 1 giải Bạc.",
            "icon": "fas fa-globe-asia",
            "tags": "ASMO, Indonesia",
            "category": "competition",
            "color": "green",
            "is_stat": False,
            "is_card": True,
            "order": 13,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "Dấu ấn tri thức & hội nhập quốc tế",
            "stat_value": "",
            "stat_label": "",
            "description": "Trên 50% học sinh K12 đạt IELTS 5.0-7.5 & HSK 3-6. 15 học sinh đạt học bổng du học cao.",
            "icon": "fas fa-star",
            "tags": "IELTS, HSK, Scholarship",
            "category": "language",
            "color": "purple",
            "is_stat": False,
            "is_card": True,
            "order": 14,
            "year": 2025,
            "is_active": True,
        },
        {
            "title": "Tỷ lệ đỗ đại học hàng đầu",
            "stat_value": "",
            "stat_label": "",
            "description": "Trên 98% học sinh K12 đỗ vào các trường Đại học hàng đầu Việt Nam.",
            "icon": "fas fa-user-graduate",
            "tags": "Top University",
            "category": "academic",
            "color": "pink",
            "is_stat": False,
            "is_card": True,
            "order": 15,
            "year": 2025,
            "is_active": True,
        },
    ]

    active_ids = []
    for payload in records:
        obj, _ = Achievement.objects.update_or_create(
            title=payload["title"],
            year=payload["year"],
            is_stat=payload["is_stat"],
            defaults=payload,
        )
        active_ids.append(obj.id)

    Achievement.objects.exclude(id__in=active_ids).update(is_active=False)
    print(f"[OK] Synced Achievement: {len(active_ids)} active records")


def upsert_pillars():
    records = [
        {
            "title": "Học Làm Người",
            "icon": "fas fa-heart",
            "short_description": "Nuôi dưỡng và định hình nhân cách, tình yêu đất nước, giá trị bản thân; phát triển năng lực cảm xúc xã hội SEL và giá trị sống theo mô thức GRACE.",
            "order": 1,
        },
        {
            "title": "Vững Vàng Tri Thức",
            "icon": "fas fa-book-open",
            "short_description": "Trang bị kiến thức Văn hóa, Khoa học, Toán tư duy từ nền tảng đến chuyên biệt; làm chủ công nghệ mới và trí tuệ nhân tạo (AI), thành thạo ít nhất 2 ngoại ngữ khi tốt nghiệp.",
            "order": 2,
        },
        {
            "title": "Thành Thục Kỹ Năng",
            "icon": "fas fa-lightbulb",
            "short_description": "Trang bị năng lực 5Cs: giao tiếp, tư duy phản biện, hợp tác, giải quyết vấn đề sáng tạo và tư duy máy tính; rèn kỹ năng thế kỷ 21 để trở thành công dân toàn cầu.",
            "order": 3,
        },
        {
            "title": "Thể Lực - Tinh Thần Lành Mạnh",
            "icon": "fas fa-dumbbell",
            "short_description": "Rèn luyện thể chất qua thể dục thể thao phù hợp lứa tuổi; phát triển nghệ thuật và lồng ghép SEL/EQ để nuôi dưỡng cảm xúc tích cực.",
            "order": 4,
        },
        {
            "title": "Học Gắn Với Hành Với Thực Tiễn Cuộc Sống",
            "icon": "fas fa-seedling",
            "short_description": "Học gắn với thực hành, đa trải nghiệm, đa phương pháp; định hướng nghề nghiệp và khởi nghiệp sớm.",
            "order": 5,
        },
        {
            "title": "Tăng Cường Năng Lực Công Nghệ - AI",
            "icon": "fas fa-microchip",
            "short_description": "Liên tục đào tạo cán bộ, giáo viên để ứng dụng hiệu quả công nghệ và AI trong dạy học, đánh giá và quản lý giáo dục.",
            "order": 6,
        },
    ]

    active_ids = []
    for payload in records:
        obj, _ = Pillar.objects.update_or_create(
            title=payload["title"],
            defaults={**payload, "is_active": True},
        )
        active_ids.append(obj.id)

    Pillar.objects.exclude(id__in=active_ids).update(is_active=False)
    print(f"[OK] Synced Pillar: {len(active_ids)} active records")


def upsert_founder_message():
    full_message = (
        "Trong kỷ nguyên số hóa và hội nhập toàn cầu, giáo dục không chỉ dừng lại ở việc truyền thụ tri thức,\n\n"
        "mà phải là hành trình khơi mở tiềm năng, thắp lửa đam mê và kiến tạo nên những cá tính độc đáo.\n\n"
        "\"Khác biệt tạo nên bản sắc. Khai phá khác biệt, chính là trao cho mỗi đứa trẻ cơ hội trở thành phiên bản tốt nhất của chính mình.\"\n\n"
        "Chúng tôi tin rằng, mỗi học sinh MIS là một \"hạt giống độc bản\", và chúng tôi tạo ra môi trường nơi sự khác biệt được đón nhận,\n"
        "sáng tạo được khuyến khích, lòng nhân ái cùng tinh thần toàn cầu được nuôi dưỡng mỗi ngày.\n\n"
        "MIS tự hào là ngọn cờ tiên phong trong đổi mới giáo dục Việt Nam với tinh thần Glocal - tư duy toàn cầu, bản sắc địa phương.\n"
        "Chúng tôi dạy học sinh không chỉ để giỏi mà còn để dẫn dắt cuộc đời mình và tạo giá trị cho cộng đồng.\n\n"
        "Với triết lý \"Giáo dục vì con người\", chúng tôi cam kết đồng hành để mỗi học sinh tỏa sáng trên hành trình học thuật,\n"
        "trưởng thành về nhân cách và vững vàng trước biến động của tương lai."
    )

    obj, _ = FounderMessage.objects.get_or_create(
        founder_name="ÔNG. HOÀNG VĂN LƯỢC",
        defaults={
            "founder_title": "TỔNG GIÁM ĐỐC ĐIỀU HÀNH - Hệ thống Giáo dục Đa Trí Tuệ MIS",
            "main_quote": "HỌC ĐỂ TỰ DO, SÁNG TẠO - HỌC ĐỂ HẠNH PHÚC - THÔNG MINH ĐỂ HẠNH PHÚC",
            "greeting": "Ba mẹ và các con học sinh thân mến,",
            "full_message": full_message,
            "closing_message": "Hãy đồng hành cùng chúng tôi, để khác biệt là điểm khởi đầu của vĩ đại!\n\nTrân trọng!",
            "is_active": True,
        },
    )

    obj.founder_title = "TỔNG GIÁM ĐỐC ĐIỀU HÀNH - Hệ thống Giáo dục Đa Trí Tuệ MIS"
    obj.main_quote = "HỌC ĐỂ TỰ DO, SÁNG TẠO - HỌC ĐỂ HẠNH PHÚC - THÔNG MINH ĐỂ HẠNH PHÚC"
    obj.greeting = "Ba mẹ và các con học sinh thân mến,"
    obj.full_message = full_message
    obj.closing_message = "Hãy đồng hành cùng chúng tôi, để khác biệt là điểm khởi đầu của vĩ đại!\n\nTrân trọng!"
    obj.is_active = True
    obj.save()

    FounderMessage.objects.exclude(id=obj.id).update(is_active=False)
    print("[OK] Synced FounderMessage")


def _save_testimonial_photo(obj, static_rel_path):
    static_path = Path(static_rel_path)
    if not static_path.exists():
        raise FileNotFoundError(f"Missing static image: {static_path}")

    filename = static_path.name
    if obj.photo and obj.photo.name.endswith(filename):
        return

    with static_path.open("rb") as image_handle:
        obj.photo.save(filename, File(image_handle), save=False)


def upsert_testimonials():
    records = [
        {
            "parent_name": "PHHS Đức Minh",
            "student_class": "2S2",
            "title": "Phụ huynh chia sẻ về hành trình học tập",
            "short_quote": "Tôi tiếp xúc với các bạn học sinh ở trường MIS ở các cấp học thì tôi thấy rằng nổi bật lên là có sự tự tin. Các bạn được thể hiện năng lực, cá tính của mình, cũng như dám nói lên tiếng nói, ý kiến của các bạn.",
            "full_content": (
                "Tôi tiếp xúc với các bạn học sinh ở trường MIS ở các cấp học thì tôi thấy rằng nổi bật lên là có sự tự tin. "
                "Các bạn rất tự tin, được thể hiện năng lực, cá tính của mình, cũng như dám nói lên tiếng nói, ý kiến của các bạn. "
                "Nếu quý vị phụ huynh đang tìm một môi trường đủ tốt, đủ an toàn để các con thể hiện bản thân, bồi đắp sự tự tin "
                "và nuôi dưỡng tình yêu thương thì đây là môi trường rất phù hợp."
            ),
            "achievement": "",
            "video_url": "https://drive.google.com/file/d/1iGOvHXWkl40oZ27F1efMvJoILZVt8LYe/preview",
            "has_video": True,
            "order": 1,
            "static_photo": "static/images/testimonials/phhs-duc-minh.png",
        },
        {
            "parent_name": "PHHS Lương Mỹ Cầm",
            "student_class": "12A5",
            "title": "Học bằng cả trí tuệ và cảm xúc",
            "short_quote": "Hành trình con đi cùng với nhà trường là 03 năm, tôi thấy quyết định của mình rất đúng đắn. Con được học bằng cả trí tuệ và cảm xúc, phát triển không chỉ kiến thức mà còn nhân cách.",
            "full_content": (
                "Hành trình con đi cùng với nhà trường là 03 năm, tôi thấy quyết định của mình rất đúng đắn. "
                "Con được học bằng cả trí tuệ và cảm xúc, phát triển không chỉ về kiến thức mà còn về nhân cách."
            ),
            "achievement": "Học sinh giỏi tiếng Trung cấp Thành phố & HSK6 năm lớp 11",
            "video_url": "https://drive.google.com/file/d/1hmRtxqseOGkH1Ao_LAKmAC_cgv575Gqw/preview",
            "has_video": True,
            "order": 2,
            "static_photo": "static/images/testimonials/phhs-my-cam.png",
        },
        {
            "parent_name": "PHHS Nguyễn Ngọc Y Lăng",
            "student_class": "Khoá 2022-2025",
            "title": "Con thay đổi hoàn toàn",
            "short_quote": "Cháu em từng rất sợ Toán và không hứng thú đi học. Nhưng khi vào đây một thời gian, con thay đổi hoàn toàn, hứng thú hơn và được trân trọng bởi các tài năng riêng.",
            "full_content": (
                "Cháu em từng rất sợ Toán và không hứng thú đi học. Nhưng khi vào đây một thời gian, con thay đổi hoàn toàn, "
                "hứng thú hơn và được trân trọng bởi các tài năng riêng. Từ một người rất sợ Toán, bây giờ con có thành tích gần như đứng đầu lớp."
            ),
            "achievement": "HSK5 - Học bổng toàn phần ĐH Ngôn ngữ Bắc Kinh",
            "video_url": "https://drive.google.com/file/d/15EpTXJidE-PNZ8d6ZXWfXhutyzZcvFaW/preview",
            "has_video": True,
            "order": 3,
            "static_photo": "static/images/testimonials/phhs-y-lang.png",
        },
    ]

    active_ids = []
    for payload in records:
        static_photo = payload.pop("static_photo")
        key = {
            "parent_name": payload["parent_name"],
            "student_class": payload["student_class"],
        }
        obj, _ = ParentTestimonial.objects.get_or_create(**key)
        for field, value in payload.items():
            setattr(obj, field, value)
        obj.is_active = True
        _save_testimonial_photo(obj, static_photo)
        obj.save()
        active_ids.append(obj.id)

    ParentTestimonial.objects.exclude(id__in=active_ids).update(is_active=False)
    print(f"[OK] Synced ParentTestimonial: {len(active_ids)} active records")


def main():
    upsert_achievements()
    upsert_pillars()
    upsert_founder_message()
    upsert_testimonials()
    print("[DONE] Home content DB sync completed")


main()
