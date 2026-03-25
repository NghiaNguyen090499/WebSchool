"""
Management command to create sample sections for the Why MIS page.
Run with: python manage.py setup_whymis
"""
from django.core.management.base import BaseCommand
from about.models import AboutPage, AboutSection


class Command(BaseCommand):
    help = 'Create sample sections for the Why MIS page'

    def handle(self, *args, **options):
        # Get or create the whymis page
        page, created = AboutPage.objects.get_or_create(
            page_type='whymis',
            defaults={
                'title': 'Tại Sao Chọn MIS?',
                'content': 'Giáo dục khai phóng 4.0 với Đa Trí Tuệ Gardner, hệ giá trị GRACE và lộ trình cá nhân hóa cho mỗi học sinh.'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created page: whymis'))
        else:
            self.stdout.write('Page already exists: whymis')
        
        # Clear existing sections if user confirms
        existing_count = page.sections.count()
        if existing_count > 0:
            self.stdout.write(f'Found {existing_count} existing sections.')
            # Keep existing sections, just update if needed
        
        sections_data = [
            # 1. Hero Section
            {
                'order': 1,
                'layout': 'hero',
                'background': 'gradient',
                'eyebrow': 'Tại Sao Chọn MIS?',
                'title': 'Kiến Tạo Tương Lai',
                'highlight_text': 'Công Dân Toàn Cầu',
                'subtitle': 'Giáo dục khai phóng 4.0 với Đa Trí Tuệ Gardner, hệ giá trị GRACE và lộ trình cá nhân hóa cho mỗi học sinh',
                'cta_text': 'Khám Phá MIS',
                'cta_url': '#differentiators',
            },
            # 2. Stats Section
            {
                'order': 2,
                'layout': 'stats',
                'background': 'white',
                'title': 'Thành Tựu Nổi Bật',
                'kpi': '''15+ Năm Kinh Nghiệm
98% Đậu ĐH Top
500+ Học Sinh/Năm
50+ Học Bổng/Năm''',
            },
            # 3. Features/Differentiators Section
            {
                'order': 3,
                'layout': 'features',
                'background': 'light',
                'eyebrow': 'Điểm Khác Biệt',
                'title': 'Tại Sao Phụ Huynh Tin Tưởng MIS?',
                'subtitle': 'MIS kết hợp triết lý giáo dục tiên tiến với phương pháp thực hành hiện đại, mang đến cho học sinh nền tảng vững chắc cho tương lai',
                'content': '''• Đa Trí Tuệ Gardner - Khám phá và phát triển 9 loại hình trí tuệ
• Song Ngữ Quốc Tế - IELTS 6.0-7.5+ và HSK 4-6 
• STEAM & Robotics - Công nghệ sáng tạo, AI, kỹ năng số
• Giá Trị GRACE - Gratitude (Biết ơn), Respect (Tôn trọng), Accountability (Trách nhiệm), Courage (Dũng cảm), Engagement (Kết nối)
• Nghệ Thuật & Sáng Tạo - Tâm Vận Động, TNST
• Môi Trường Nội Trú - Cơ sở vật chất hiện đại, đồng hành 24/7''',
            },
            # 4. Partners Section
            {
                'order': 4,
                'layout': 'text_left',
                'background': 'white',
                'eyebrow': 'Đối Tác Chiến Lược',
                'title': 'Hợp Tác Cùng Các Tổ Chức Giáo Dục Uy Tín',
                'content': '''MIS tự hào hợp tác với các đơn vị giáo dục hàng đầu trong và ngoài nước, mang đến cho học sinh những chương trình đào tạo chuẩn quốc tế và cơ hội kết nối toàn cầu.

• Aptech Computer Education - Đào tạo công nghệ
• Jaxtina English - Tiếng Anh chuẩn quốc tế  
• Times International School - Hợp tác giáo dục
• Quốc Tế Thời Đại - Tiếng Trung HSK''',
                'cta_text': 'Tìm Hiểu Thêm',
                'cta_url': '/about/mission/',
            },
            # 5. Testimonial Section
            {
                'order': 5,
                'layout': 'quote',
                'background': 'light',
                'title': 'Chị Nguyễn Thị Mai',
                'subtitle': 'Phụ huynh học sinh lớp 7',
                'content': 'MIS đã thay đổi con tôi hoàn toàn. Con tự tin hơn, năng động hơn và đặc biệt là yêu việc học. Tôi rất hài lòng với sự phát triển toàn diện của con tại đây.',
            },
            # 6. CTA Section
            {
                'order': 6,
                'layout': 'cta',
                'background': 'gradient',
                'title': 'Sẵn Sàng Cho Hành Trình Tuyệt Vời?',
                'subtitle': 'Đặt lịch tham quan hoặc đăng ký tư vấn ngay hôm nay để khám phá môi trường học tập lý tưởng cho con bạn',
                'cta_text': 'Đặt Lịch Tham Quan',
                'cta_url': '/contact/',
                'cta_secondary_text': 'Đăng Ký Tuyển Sinh',
                'cta_secondary_url': '/tuyen-sinh/',
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for section_data in sections_data:
            section, section_created = AboutSection.objects.update_or_create(
                page=page,
                order=section_data['order'],
                defaults=section_data
            )
            if section_created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Done! Created {created_count} sections, updated {updated_count} sections.'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Visit /about/whymis/ to see the page.'
        ))
