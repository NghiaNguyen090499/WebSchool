"""
Management command to seed sample data for new dynamic content models
"""
from django.core.management.base import BaseCommand
from core.models import HeroSlide, Achievement, ParentTestimonial, Partner, FounderMessage


class Command(BaseCommand):
    help = 'Seed sample data for dynamic homepage content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write("Clearing existing data...")
            HeroSlide.objects.all().delete()
            Achievement.objects.all().delete()
            ParentTestimonial.objects.all().delete()
            Partner.objects.all().delete()
            FounderMessage.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Cleared all existing data"))

        self.seed_hero_slides()
        self.seed_achievements()
        self.seed_founder_message()

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample data!"))

    def seed_hero_slides(self):
        """Seed hero slides"""
        slides_data = [
            {
                'title': 'Khác biệt là điểm khởi đầu',
                'title_highlight': 'của vĩ đại',
                'subtitle': 'Hệ thống Giáo dục Đa Trí Tuệ MIS',
                'slogan': 'Giáo dục con tim – Kiến tạo giá trị sống',
                'description': 'Khác biệt tạo nên bản sắc. Khai phá khác biệt, chính là trao cho mỗi đứa trẻ cơ hội trở thành phiên bản tốt nhất của chính mình.',
                'badge_text': 'Hệ thống Giáo dục Đa Trí Tuệ MIS',
                'slide_type': 'welcome',
                'cta_primary_text': 'Tìm hiểu thêm',
                'cta_primary_url': '/about/academics/',
                'cta_primary_icon': 'fas fa-arrow-right',
                'cta_secondary_text': 'Liên hệ tư vấn',
                'cta_secondary_url': '/contact/',
                'order': 1,
            },
            {
                'title': 'TUYỂN SINH NĂM HỌC',
                'title_highlight': '2025 - 2026',
                'subtitle': '',
                'slogan': 'Giáo dục con tim – Kiến tạo giá trị sống',
                'description': 'Khám phá môi trường học tập hiện đại, chương trình giáo dục tiên tiến.',
                'badge_text': 'Đang mở đăng ký',
                'badge_icon': 'fas fa-calendar-check',
                'slide_type': 'admissions',
                'cta_primary_text': 'Đăng ký ngay',
                'cta_primary_url': '/tuyen-sinh/',
                'cta_primary_icon': 'fas fa-arrow-right',
                'cta_secondary_text': 'Xem học phí',
                'cta_secondary_url': '/tuyen-sinh/',
                'order': 2,
            },
            {
                'title': 'CHƯƠNG TRÌNH STEAM',
                'title_highlight': '& CÔNG NGHỆ CAO',
                'subtitle': '',
                'slogan': 'Giáo dục con tim – Kiến tạo giá trị sống',
                'description': 'Đón đầu kỷ nguyên 4.0 với tư duy sáng tạo và kỹ năng công nghệ vượt trội.',
                'badge_text': 'Chương trình đặc biệt',
                'badge_icon': 'fas fa-robot',
                'slide_type': 'program',
                'cta_primary_text': 'Khám phá STEAM',
                'cta_primary_url': '/about/steam/',
                'cta_primary_icon': 'fas fa-arrow-right',
                'order': 3,
            },
            {
                'title': 'TÀI NĂNG TIẾNG TRUNG',
                'title_highlight': '& TIẾNG ANH',
                'subtitle': '',
                'slogan': 'Giáo dục con tim – Kiến tạo giá trị sống',
                'description': 'Chinh phục ngoại ngữ thứ 2, sẵn sàng hội nhập toàn cầu với cam kết IELTS 7.0+ & HSK5+.',
                'badge_text': 'Du học Trung Quốc',
                'badge_icon': 'fas fa-globe',
                'slide_type': 'program',
                'cta_primary_text': 'Tìm hiểu ngay',
                'cta_primary_url': '/about/',
                'cta_primary_icon': 'fas fa-arrow-right',
                'order': 4,
            },
        ]

        for data in slides_data:
            slide, created = HeroSlide.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"  Created HeroSlide: {slide.title}")
            else:
                self.stdout.write(f"  HeroSlide already exists: {slide.title}")

    def seed_achievements(self):
        """Seed achievements - stats and cards"""
        achievements_data = [
            # Stats
            {
                'stat_value': '98%',
                'stat_label': 'Tỷ lệ đậu Đại học',
                'title': 'Kết quả học tập xuất sắc',
                'description': 'Học sinh MIS đạt tỷ lệ đậu Đại học cao với nhiều em nhận học bổng',
                'icon': 'fas fa-graduation-cap',
                'category': 'academic',
                'color': 'red',
                'is_stat': True,
                'is_card': False,
                'order': 1,
            },
            {
                'stat_value': '8.0',
                'stat_label': 'IELTS cao nhất',
                'title': 'Năng lực tiếng Anh vượt trội',
                'description': 'Học sinh THPT đạt điểm IELTS cao nhất lên đến 8.0',
                'icon': 'fas fa-language',
                'category': 'language',
                'color': 'amber',
                'is_stat': True,
                'is_card': False,
                'order': 2,
            },
            {
                'stat_value': 'HSK6',
                'stat_label': 'Chứng chỉ Hoa ngữ',
                'title': 'Thành thạo tiếng Trung',
                'description': 'Học sinh đạt HSK6 - trình độ cao nhất của kỳ thi Hán ngữ Quốc tế',
                'icon': 'fas fa-book-reader',
                'category': 'language',
                'color': 'red',
                'is_stat': True,
                'is_card': False,
                'order': 3,
            },
            {
                'stat_value': '50+',
                'stat_label': 'Giải thưởng Quốc tế',
                'title': 'Thành tích thi đấu',
                'description': 'Hơn 50 giải thưởng tại các cuộc thi Olympic Toán, Khoa học quốc tế',
                'icon': 'fas fa-trophy',
                'category': 'competition',
                'color': 'amber',
                'is_stat': True,
                'is_card': False,
                'order': 4,
            },
            # Cards
            {
                'stat_value': '#1',
                'stat_label': 'Robotics Malaysia',
                'title': 'STEAM & Robotics',
                'description': 'Giải thưởng cuộc thi Robotics Quốc tế Malaysia 2025, đưa MIS lên bản đồ STEAM khu vực Đông Nam Á',
                'tags': 'Giải Nhất, Malaysia 2025',
                'icon': 'fas fa-robot',
                'category': 'competition',
                'color': 'red',
                'is_stat': False,
                'is_card': True,
                'order': 5,
            },
            {
                'stat_value': '30+',
                'stat_label': 'Huy chương',
                'title': 'Olympic Toán - Khoa học',
                'description': 'Liên tục đạt giải cao tại các cuộc thi ASMO, SASMO, Kangaroo Math với nhiều huy chương Vàng, Bạc',
                'tags': 'ASMO, Kangaroo, SASMO',
                'icon': 'fas fa-trophy',
                'category': 'competition',
                'color': 'amber',
                'is_stat': False,
                'is_card': True,
                'order': 6,
            },
            {
                'stat_value': '100%',
                'stat_label': 'Học bổng',
                'title': 'Ngôn ngữ & Học bổng',
                'description': 'Học sinh đạt IELTS 8.0, HSK 3-6, nhiều em nhận học bổng toàn phần các trường đại học quốc tế',
                'tags': 'IELTS, HSK, Học bổng',
                'icon': 'fas fa-language',
                'category': 'scholarship',
                'color': 'red',
                'is_stat': False,
                'is_card': True,
                'order': 7,
            },
        ]

        for data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f"  Created Achievement: {achievement.title}")
            else:
                self.stdout.write(f"  Achievement already exists: {achievement.title}")

    def seed_founder_message(self):
        """Seed founder message"""
        if FounderMessage.objects.exists():
            self.stdout.write("  FounderMessage already exists, skipping...")
            return

        message = FounderMessage.objects.create(
            founder_name='Ông. Hoàng Văn Lược',
            founder_title='Tổng Giám đốc Điều hành\nHệ thống Giáo dục Đa Trí Tuệ MIS',
            main_quote='Khác biệt tạo nên bản sắc. Khai phá khác biệt, chính là trao cho mỗi đứa trẻ cơ hội trở thành phiên bản tốt nhất của chính mình.',
            greeting='Ba mẹ và các con học sinh thân mến,',
            full_message='''Trong thời đại số hóa và toàn cầu hóa, giáo dục không chỉ là truyền đạt kiến thức mà còn là khơi dậy tiềm năng, đam mê và cá tính riêng biệt của mỗi học sinh.

Tại MIS, chúng tôi tin rằng mỗi học sinh là một "hạt giống độc đáo". Chúng tôi tạo ra môi trường nơi sự khác biệt được tôn trọng, sáng tạo được khuyến khích, và lòng nhân ái cùng tinh thần toàn cầu được nuôi dưỡng mỗi ngày.

MIS là tiên phong trong đổi mới giáo dục tại Việt Nam với tư duy "Glocal" - tư duy toàn cầu, bản sắc địa phương, chuẩn bị cho những cá nhân có thể tư duy độc lập, yêu thương, kết nối và đứng vững trước mọi thay đổi.

Chương trình giáo dục tại MIS được thiết kế theo triết lý "Giáo dục con tim - Kiến tạo giá trị sống", kết hợp hài hòa giữa kiến thức nền tảng vững chắc với các kỹ năng thế kỷ 21, năng lực công nghệ và trí tuệ cảm xúc.''',
            closing_message='Hãy đồng hành cùng chúng tôi, để khác biệt là điểm khởi đầu của vĩ đại!',
            is_active=True,
        )
        self.stdout.write(f"  Created FounderMessage: {message.founder_name}")
