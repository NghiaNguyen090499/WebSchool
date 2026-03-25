"""
Management command to add sample data for MIS website
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import CoreValue, Statistic, MenuItem
from news.models import News, Category
from events.models import Event
from gallery.models import Album, Photo
from about.models import AboutPage


class Command(BaseCommand):
    help = 'Add sample data for MIS website (Statistics, Core Values, News, Events, Gallery, About)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Adding sample data...'))
        
        # 1. Add Statistics
        self.add_statistics()
        
        # 2. Add Core Values
        self.add_core_values()
        
        # 3. Add News & Categories
        self.add_news()
        
        # 4. Add Events
        self.add_events()
        
        # 5. Add Gallery
        self.add_gallery()
        
        # 6. Add Menus
        self.add_menus()
        
        # 7. Add About Pages
        self.add_about_pages()
        
        self.stdout.write(self.style.SUCCESS('\nAll sample data added successfully!'))

    def add_menus(self):
        self.stdout.write("Adding Menus...")
        # Clear existing
        MenuItem.objects.all().delete()
        
        # Structure based on misvn.edu.vn - Full navigation with correct URLs
        menus = [
            {
                'title': 'GIỚI THIỆU', 'link': '#', 'icon': 'fas fa-info-circle', 'order': 1,
                'children': [
                    {'title': 'Giới thiệu chung về MIS', 'link': '/about/mission/', 'icon': 'fas fa-info'},
                    {'title': '8 điểm mạnh khác biệt', 'link': '/about/strengths/', 'icon': 'fas fa-star'},
                    {'title': 'Thông điệp Tổng Giám đốc', 'link': '/about/principal/', 'icon': 'fas fa-envelope'},
                    {'title': 'Chiến lược phát triển', 'link': '/about/strategy/'},
                    {'title': 'Cơ cấu tổ chức MIS', 'link': '/about/structure/', 'icon': 'fas fa-sitemap'},
                    {'title': 'Quy định văn hóa MIS', 'link': '/about/culture/'},
                    {'title': 'Môi trường nội trú', 'link': '/about/boarding/', 'icon': 'fas fa-bed'},
                    {'title': 'Giáo dục khai phóng', 'link': '/about/liberal/'},
                ]
            },
            {
                'title': 'CHƯƠNG TRÌNH HỌC', 'link': '#', 'icon': 'fas fa-book', 'order': 2,
                'children': [
                    {'title': 'Mầm non – Tiền tiểu học', 'link': '/tuyen-sinh/mam_non/', 'icon': 'fas fa-baby'},
                    {'title': 'Chương trình môn Toán', 'link': '/about/curriculum/math/', 'icon': 'fas fa-calculator'},
                    {'title': 'Chương trình môn Ngữ văn', 'link': '/about/curriculum/literature/', 'icon': 'fas fa-book-open'},
                    {'title': 'Chương trình Tiếng Anh', 'link': '/about/curriculum/english/', 'icon': 'fas fa-globe'},
                    {'title': 'Chương trình Tiếng Trung', 'link': '/about/curriculum/chinese/'},
                    {'title': 'Chương trình STEAM', 'link': '/about/curriculum/steam/', 'icon': 'fas fa-cogs'},
                    {'title': 'Chương trình Robotic', 'link': '/about/curriculum/robotics/', 'icon': 'fas fa-robot'},
                    {'title': 'Kỹ năng sống', 'link': '/about/curriculum/lifeskills/', 'icon': 'fas fa-heart'},
                    {'title': 'Trải nghiệm sáng tạo (TNST)', 'link': '/about/curriculum/creative/'},
                ]
            },
            {
                'title': 'TIN TỨC', 'link': '/news/', 'icon': 'fas fa-newspaper', 'order': 3,
                'children': [
                    {'title': 'Tin nhà trường', 'link': '/news/', 'icon': 'fas fa-school'},
                ]
            },
            {
                'title': 'TUYỂN SINH', 'link': '/tuyen-sinh/', 'icon': 'fas fa-file-signature', 'order': 4,
                'children': [
                    {'title': 'Tại sao chọn MIS?', 'link': '/about/whymis/', 'icon': 'fas fa-question-circle'},
                    {'title': 'Tuyển sinh Mầm non 2025-2026', 'link': '/tuyen-sinh/mam_non/', 'icon': 'fas fa-baby'},
                    {'title': 'Tuyển sinh Tiểu học 2026-2027', 'link': '/tuyen-sinh/tieu_hoc/', 'icon': 'fas fa-child'},
                    {'title': 'Tuyển sinh THCS 2026-2027', 'link': '/tuyen-sinh/thcs/', 'icon': 'fas fa-user-graduate'},
                    {'title': 'Tuyển sinh THPT 2026-2027', 'link': '/tuyen-sinh/thpt/', 'icon': 'fas fa-graduation-cap'},
                    {'title': 'Đăng ký trực tuyến', 'link': '/tuyen-sinh/', 'icon': 'fas fa-edit'},
                ]
            },
            {
                'title': 'NHỊP SỐNG HỌC ĐƯỜNG', 'link': '#', 'icon': 'fas fa-camera', 'order': 5,
                'children': [
                    {'title': 'Tiếng nói Misers', 'link': '#', 'icon': 'fas fa-microphone'},
                    {'title': 'Gương mặt Misers', 'link': '#', 'icon': 'fas fa-user-circle'},
                    {'title': 'Y tế & Tâm lý học đường', 'link': '#', 'icon': 'fas fa-heartbeat'},
                    {'title': 'Tư vấn – Hướng nghiệp', 'link': '#', 'icon': 'fas fa-compass'},
                    {'title': 'Sự kiện', 'link': '/events/', 'icon': 'fas fa-calendar-alt'},
                    {'title': 'Thư viện ảnh', 'link': '/gallery/', 'icon': 'fas fa-images'},
                    {'title': 'Hoạt động ngoại khóa', 'link': '#', 'icon': 'fas fa-running'},
                ]
            }
        ]
        
        
        def create_item(data, parent=None):
            children = data.pop('children', [])
            item = MenuItem.objects.create(**data, parent=parent, position='header')
            for child_data in children:
                create_item(child_data, parent=item)

        for item_data in menus:
            create_item(item_data)
        
        self.stdout.write(f"  + Added Menu Items: {MenuItem.objects.count()}")

    def add_statistics(self):
        # Xóa tất cả statistics cũ để tránh trùng lặp
        Statistic.objects.all().delete()
        
        statistics_data = [
            {'label': 'Năm kinh nghiệm', 'value': 28, 'icon': 'fas fa-award', 'order': 1},
            {'label': 'Học sinh giỏi', 'value': 3000, 'icon': 'fas fa-user-graduate', 'order': 2},
            {'label': 'Giáo viên', 'value': 200, 'icon': 'fas fa-chalkboard-teacher', 'order': 3},
            {'label': 'Đỗ Đại học (%)', 'value': 98, 'icon': 'fas fa-trophy', 'order': 4},
        ]
        
        count = 0
        for data in statistics_data:
            Statistic.objects.create(**data)
            count += 1
        self.stdout.write(f"  + Statistics: Created {count} items")

    def add_core_values(self):
        # VALUES: Tôn trọng, Yêu thương, Kỷ cương, Trách nhiệm, Trung thực, Hợp tác, Sáng tạo, Khát vọng
        values_data = [
            {'title': 'Tôn trọng', 'description': 'Tôn trọng bản thân, tôn trọng người khác và tôn trọng môi trường sống.', 'icon': 'fas fa-hand-holding-heart'},
            {'title': 'Yêu thương', 'description': 'Biết yêu thương, sẻ chia và giúp đỡ mọi người xung quanh.', 'icon': 'fas fa-heart'},
            {'title': 'Sáng tạo', 'description': 'Luôn tìm tòi, đổi mới và phát huy năng lực tư duy sáng tạo.', 'icon': 'fas fa-lightbulb'},
            {'title': 'Trách nhiệm', 'description': 'Dám nghĩ, dám làm và dám chịu trách nhiệm về hành động của mình.', 'icon': 'fas fa-tasks'},
            {'title': 'Trung thực', 'description': 'Sống ngay thẳng, thật thà và dũng cảm nhận lỗi.', 'icon': 'fas fa-balance-scale'},
            {'title': 'Hợp tác', 'description': 'Đoàn kết, tương trợ và cùng nhau phát triển.', 'icon': 'fas fa-users'},
            {'title': 'Kỷ cương', 'description': 'Tự giác chấp hành nội quy và rèn luyện nề nếp.', 'icon': 'fas fa-gavel'},
            {'title': 'Khát vọng', 'description': 'Luôn nỗ lực vươn lên để đạt được những ước mơ cao đẹp.', 'icon': 'fas fa-star'},
        ]

        count = 0
        for data in values_data:
            _, created = CoreValue.objects.get_or_create(title=data['title'], defaults=data)
            if created: count += 1
        self.stdout.write(f"  + Core Values: Added {count} new items")

    def add_news(self):
        # Create Categories matching education levels
        categories_data = [
            {'name': 'Tin nhà trường', 'slug': 'tin-nha-truong'},
            {'name': 'Tiểu học', 'slug': 'tieu-hoc'},
            {'name': 'THCS', 'slug': 'thcs'},
            {'name': 'THPT', 'slug': 'thpt'},
            {'name': 'Tuyển sinh', 'slug': 'tuyen-sinh'},
            {'name': 'Thông báo', 'slug': 'thong-bao'},
        ]
        cats = {}
        for data in categories_data:
            cat, _ = Category.objects.get_or_create(slug=data['slug'], defaults={'name': data['name']})
            cats[data['slug']] = cat
        
        # Create News for each category
        news_data = [
            # Featured
            {'title': 'Lễ khai giảng năm học 2025-2026', 'content': 'Sáng nay, trường MIS long trọng tổ chức lễ khai giảng...', 'excerpt': 'Không khí tưng bừng của ngày hội đến trường', 'category': cats['tin-nha-truong'], 'is_featured': True},
            # Tiểu học
            {'title': 'Học sinh Tiểu học đạt giải cuộc thi Toán Violympic', 'content': 'Chúc mừng các em Tiểu học...', 'excerpt': 'Thành tích vượt trội trong cuộc thi Toán online', 'category': cats['tieu-hoc'], 'is_featured': False},
            {'title': 'Ngày hội đọc sách khối Tiểu học', 'content': 'Ngày hội đọc sách diễn ra...', 'excerpt': 'Lan tỏa văn hóa đọc tại khối Tiểu học', 'category': cats['tieu-hoc'], 'is_featured': False},
            # THCS
            {'title': 'Học sinh THCS giành Huy chương Vàng Olympic Tiếng Anh', 'content': 'Chúc mừng em học sinh...', 'excerpt': 'Thành tích xuất sắc tại Olympic Tiếng Anh cấp thành phố', 'category': cats['thcs'], 'is_featured': False},
            {'title': 'Cuộc thi khoa học kỹ thuật dành cho học sinh THCS', 'content': 'Các em học sinh tham gia...', 'excerpt': 'Phát huy tinh thần sáng tạo STEM', 'category': cats['thcs'], 'is_featured': False},
            # THPT
            {'title': 'Học sinh THPT đạt giải Quốc gia môn Vật lý', 'content': 'Niềm vui lớn...', 'excerpt': 'Vinh danh tài năng Vật lý của MIS', 'category': cats['thpt'], 'is_featured': False},
            {'title': 'Tư vấn hướng nghiệp cho học sinh lớp 12', 'content': 'Chương trình tư vấn diễn ra...', 'excerpt': 'Định hướng tương lai nghề nghiệp', 'category': cats['thpt'], 'is_featured': False},
            # Tuyển sinh
            {'title': 'Thông báo tuyển sinh lớp 1 năm học 2026-2027', 'content': 'Nhà trường thông báo kế hoạch...', 'excerpt': 'Chỉ tiêu và quy trình tuyển sinh', 'category': cats['tuyen-sinh'], 'is_featured': False},
            {'title': 'Mở đăng ký tuyển sinh lớp 6 năm học 2026-2027', 'content': 'Nhà trường mở đăng ký...', 'excerpt': 'Đăng ký sớm nhận ưu đãi', 'category': cats['tuyen-sinh'], 'is_featured': False},
            {'title': 'Chính sách học bổng cho học sinh giỏi', 'content': 'Nhà trường có chính sách...', 'excerpt': 'Cơ hội nhận học bổng hấp dẫn', 'category': cats['tuyen-sinh'], 'is_featured': False},
        ]

        count = 0
        for data in news_data:
            if not News.objects.filter(title=data['title']).exists():
                News.objects.create(**data)
                count += 1
        self.stdout.write(f"  + News: Added {count} new items")

    def add_events(self):
        events_data = [
            {
                'title': 'Ngày hội Open Day',
                'date': timezone.now().date() + timezone.timedelta(days=7),
                'location': 'Sân trường MIS',
                'description': 'Cơ hội tham quan và tìm hiểu môi trường học tập tại MIS.',
                'time': '08:00',
                'is_featured': True
            },
            {
                'title': 'Hội thảo: Đồng hành cùng con vào lớp 1',
                'date': timezone.now().date() + timezone.timedelta(days=14),
                'location': 'Hội trường A',
                'description': 'Chia sẻ kinh nghiệm và giải đáp thắc mắc cho phụ huynh.',
                'time': '14:00',
                'is_featured': False
            },
            {
                'title': 'Giải bóng đá MIS Cup 2025',
                'date': timezone.now().date() + timezone.timedelta(days=30),
                'location': 'Sân vận động',
                'description': 'Giải bóng đá thường niên dành cho học sinh.',
                'time': '07:30',
                'is_featured': False
            }
        ]

        count = 0
        for data in events_data:
            if not Event.objects.filter(title=data['title']).exists():
                Event.objects.create(**data)
                count += 1
        self.stdout.write(f"  + Events: Added {count} new items")

    def add_gallery(self):
        albums_data = [
            {'name': 'Hoạt động ngoại khóa Hè 2024', 'description': 'Những khoảnh khắc đáng nhớ mùa hè'},
            {'name': 'Lễ tốt nghiệp 2024', 'description': 'Chúc mừng các tân cử nhân'},
            {'name': 'Cuộc thi Rung chuông vàng', 'description': 'Sân chơi trí tuệ bổ ích'},
            {'name': 'Festival Tiếng Anh', 'description': 'Ngày hội ngôn ngữ'},
        ]

        count = 0
        for data in albums_data:
            album, created = Album.objects.get_or_create(name=data['name'], defaults=data)
            if created: count += 1
            
            # Add placeholder photos if album is empty
            if album.photos.count() == 0:
                for i in range(3):
                    Photo.objects.create(
                        album=album,
                        caption=f"Ảnh {i+1} - {album.name}",
                        order=i
                    )
        self.stdout.write(f"  + Gallery: Added {count} albums")

    def add_about_pages(self):
        about_data = [
            {
                'page_type': 'mission',
                'title': 'Giới thiệu chung về MIS',
                'content': '''Hệ thống Giáo dục MIS (Multiple Intelligences School) được thành lập với sứ mệnh:

🎯 Phát triển toàn diện tiềm năng của mỗi học sinh thông qua phương pháp giáo dục Đa Trí Tuệ.

🎯 Trang bị cho học sinh những kỹ năng cần thiết để thành công trong thế kỷ 21.

🎯 Xây dựng môi trường học tập an toàn, thân thiện và sáng tạo.

🎯 Khơi dậy niềm đam mê học tập suốt đời trong mỗi học sinh.

Chúng tôi tin rằng mỗi học sinh đều có những năng lực và tiềm năng riêng biệt, và nhiệm vụ của giáo dục là khám phá và phát triển những tiềm năng đó.'''
            },
            {
                'page_type': 'vision',
                'title': 'Hệ thống Giáo dục MIS',
                'content': '''Hệ thống Giáo dục MIS hướng tới trở thành:

🌟 Hệ thống giáo dục hàng đầu Việt Nam về ứng dụng lý thuyết Đa Trí Tuệ.

🌟 Nơi mỗi học sinh được tôn trọng, yêu thương và phát triển toàn diện.

🌟 Môi trường giáo dục hiện đại, sáng tạo và hội nhập quốc tế.

📚 GIÁ TRỊ CỐT LÕI
• Tôn trọng - Yêu thương - Kỷ cương
• Trách nhiệm - Trung thực - Hợp tác
• Sáng tạo - Khát vọng'''
            },
            {
                'page_type': 'principal',
                'title': 'Thông điệp từ Tổng Giám đốc Điều hành',
                'content': '''Kính gửi Quý Phụ huynh và các em Học sinh thân mến,

Chào mừng các bạn đến với Hệ thống Giáo dục MIS!

Tại MIS, chúng tôi tin rằng mỗi em học sinh là một cá thể độc đáo với những năng lực và tiềm năng riêng biệt.

✨ Chúng tôi cam kết:
• Tạo môi trường học tập an toàn, thân thiện
• Phát triển toàn diện các loại trí tuệ của học sinh
• Đổi mới phương pháp giảng dạy liên tục

Trân trọng,
Tổng Giám đốc Điều hành MIS'''
            },
            {
                'page_type': 'strengths',
                'title': '8 Điểm Mạnh Khác Biệt Vượt Trội của MIS',
                'content': '''🏆 8 ĐIỂM MẠNH KHÁC BIỆT CỦA HỆ THỐNG GIÁO DỤC MIS

1️⃣ PHƯƠNG PHÁP ĐA TRÍ TUỆ
Áp dụng lý thuyết Đa Trí Tuệ (Multiple Intelligences) của Howard Gardner, đánh giá và phát triển toàn diện 8 loại trí tuệ.

2️⃣ GIÁO VIÊN CHẤT LƯỢNG CAO
100% giáo viên có trình độ đại học trở lên, được đào tạo bài bản về phương pháp giảng dạy hiện đại.

3️⃣ CƠ SỞ VẬT CHẤT HIỆN ĐẠI
Phòng học thông minh, phòng lab, thư viện, sân thể thao đạt chuẩn quốc tế.

4️⃣ CHƯƠNG TRÌNH SONG NGỮ
Chương trình Anh - Việt song song, tăng cường Tiếng Anh với giáo viên bản ngữ.

5️⃣ HOẠT ĐỘNG NGOẠI KHÓA ĐA DẠNG
Hơn 30 câu lạc bộ, nhiều sự kiện văn hóa, thể thao quanh năm.

6️⃣ MÔI TRƯỜNG NỘI TRÚ CHUẨN QUỐC TẾ
Ký túc xá tiện nghi, an toàn, bồi dưỡng kỹ năng sống tự lập.

7️⃣ TƯ VẤN TÂM LÝ CHUYÊN NGHIỆP
Đội ngũ chuyên gia tâm lý hỗ trợ học sinh 24/7.

8️⃣ KẾT NỐI PHỤ HUYNH THƯỜNG XUYÊN
App quản lý học sinh, họp phụ huynh định kỳ, báo cáo tiến bộ hàng tháng.'''
            },
            {
                'page_type': 'strategy',
                'title': 'Chiến Lược Phát Triển của HTGD MIS',
                'content': '''📈 CHIẾN LƯỢC PHÁT TRIỂN HTGD MIS

🎯 TẦM NHÌN 2030
Trở thành hệ thống giáo dục dẫn đầu Việt Nam về ứng dụng Đa Trí Tuệ.

📋 MỤC TIÊU CHIẾN LƯỢC
• Mở rộng hệ thống lên 10 cơ sở trên toàn quốc
• Đạt chứng nhận quốc tế về chất lượng giáo dục
• 100% học sinh đạt chuẩn đầu ra Tiếng Anh B2

🚀 CÁC TRỤNG CỘT PHÁT TRIỂN
1. Nâng cao chất lượng đội ngũ giáo viên
2. Đầu tư công nghệ giáo dục hiện đại
3. Mở rộng hợp tác quốc tế
4. Phát triển chương trình STEAM'''
            },
            {
                'page_type': 'structure',
                'title': 'Cơ Cấu Tổ Chức MIS',
                'content': '''🏛️ CƠ CẤU TỔ CHỨC HỆ THỐNG GIÁO DỤC MIS

📌 BAN LÃNH ĐẠO
• Tổng Giám đốc Điều hành
• Trợ lý Tổng Giám đốc

📌 CÁC KHỐI CHỨC NĂNG
• Ban Giám hiệu
• Khối Hành chính văn phòng
• Phòng Giáo vụ

📌 CÁC KHỐI CHUYÊN MÔN
• Khối Tiểu học
• Khối Khoa học tự nhiên
• Khối Khoa học xã hội
• Khối Tiếng Anh
• Khối Vận động – Nghệ thuật
• Ban Phong trào – Đoàn đội

📌 TRUNG TÂM HỖ TRỢ
• Trung tâm Tư vấn Tâm lý và Thực hành TTCX-KNS
• Phòng Chuyển đổi số & Giám định chất lượng'''
            },
            {
                'page_type': 'culture',
                'title': 'Quy Định Văn Hóa MIS',
                'content': '''📜 QUY ĐỊNH VĂN HÓA MIS VÀ QUY TẮC ỨNG XỬ

🌟 GIÁ TRỊ CỐT LÕI
• Tôn trọng – Yêu thương – Kỷ cương
• Trách nhiệm – Trung thực – Hợp tác

📋 QUY TẮC ỨNG XỬ
• Đúng giờ, đúng hẹn
• Trang phục gọn gàng, đúng quy định
• Kính trọng thầy cô, yêu thương bạn bè
• Bảo vệ môi trường, giữ gìn cơ sở vật chất

💡 KHẨU HIỆU
"Học để tự do, sáng tạo – Học để Hạnh phúc – Thông minh để Hạnh phúc"'''
            },
            {
                'page_type': 'boarding',
                'title': 'Môi Trường Nội Trú MIS',
                'content': '''🏠 MÔI TRƯỜNG NỘI TRÚ MIS

Hệ thống nội trú MIS cung cấp môi trường sống và học tập an toàn, tiện nghi cho học sinh.

🛏️ TIỆN NGHI
• Phòng ở 4-6 học sinh/phòng
• Điều hòa, nóng lạnh đầy đủ
• Nhà ăn sạch sẽ, đủ dinh dưỡng
• Khu vực tự học, thư viện

👨‍👩‍👧‍👦 QUẢN LÝ 24/7
• Đội ngũ quản sinh chuyên nghiệp
• Bảo vệ an ninh xuyên suốt
• Theo dõi sức khỏe định kỳ

📚 HOẠT ĐỘNG NGOÀI GIỜ
• Lớp học kỹ năng sống
• Câu lạc bộ thể thao, nghệ thuật
• Hoạt động ngoại khóa cuối tuần'''
            },
            {
                'page_type': 'whymis',
                'title': 'Tại Sao Chọn MIS?',
                'content': '''❓ TẠI SAO PHỤ HUYNH CHỌN MIS?

✅ PHƯƠNG PHÁP GIÁO DỤC TIÊN TIẾN
Áp dụng lý thuyết Đa Trí Tuệ, phát triển toàn diện 8 loại hình trí tuệ.

✅ ĐỘI NGŨ GIÁO VIÊN CHẤT LƯỢNG
100% giáo viên có trình độ đại học, được đào tạo bài bản.

✅ CƠ SỞ VẬT CHẤT HIỆN ĐẠI
Trường học xanh, sạch, đẹp với trang thiết bị hiện đại.

✅ CHƯƠNG TRÌNH TOÀN DIỆN
Học thuật kết hợp kỹ năng sống, thể thao, nghệ thuật.

✅ HỖ TRỢ TÂM LÝ CHUYÊN NGHIỆP
Đội ngũ chuyên gia tâm lý đồng hành cùng học sinh.

✅ KẾT NỐI PHỤ HUYNH
App quản lý, báo cáo thường xuyên, họp phụ huynh định kỳ.'''
            },
            {
                'page_type': 'steam',
                'title': 'Chương Trình STEAM',
                'content': '''🔬 CHƯƠNG TRÌNH STEAM TẠI MIS

STEAM là phương pháp giáo dục tích hợp:
• Science (Khoa học)
• Technology (Công nghệ)
• Engineering (Kỹ thuật)
• Arts (Nghệ thuật)
• Mathematics (Toán học)

📚 NỘI DUNG CHƯƠNG TRÌNH
• Thí nghiệm khoa học thực hành
• Lập trình cơ bản
• Dự án nhóm sáng tạo
• Cuộc thi robotics

🎯 MỤC TIÊU
• Phát triển tư duy phản biện
• Kỹ năng giải quyết vấn đề
• Sáng tạo và đổi mới'''
            },
            {
                'page_type': 'robotics',
                'title': 'Chương Trình Robotics',
                'content': '''🤖 CHƯƠNG TRÌNH ROBOTIC TẠI MIS

Chương trình Robotics giúp học sinh làm quen với công nghệ và lập trình qua việc thiết kế, lắp ráp và điều khiển robot.

🎮 NỘI DUNG
• Lắp ráp robot Lego, Arduino
• Lập trình điều khiển cơ bản
• Tham gia cuộc thi Robotics

🏆 THÀNH TÍCH
• Giải thưởng Robotics cấp thành phố
• Học sinh đạt giải quốc gia'''
            },
        ]

        count = 0
        for data in about_data:
            _, created = AboutPage.objects.update_or_create(
                page_type=data['page_type'],
                defaults={'title': data['title'], 'content': data['content']}
            )
            if created:
                count += 1
        self.stdout.write(f"  + About Pages: Added/Updated {len(about_data)} pages")
