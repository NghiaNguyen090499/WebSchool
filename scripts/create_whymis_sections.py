# -*- coding: utf-8 -*-
"""
Script to create sample sections for the whymis page with Vietnamese
Run with: python scripts/create_whymis_sections.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from about.models import AboutPage, AboutSection

def create_sections():
    # Get or create the whymis page
    page, created = AboutPage.objects.get_or_create(
        page_type='whymis',
        defaults={
            'title': 'Tại Sao Chọn MIS?',
            'content': ''
        }
    )
    
    # Update title if page exists
    if not created:
        page.title = 'Tại Sao Chọn MIS?'
        page.save()

    # Clear existing sections
    page.sections.all().delete()

    # Create sections
    sections_data = [
        # Hero Section
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'KHÁM PHÁ MIS',
            'title': 'TẠI SAO CHỌN',
            'highlight_text': 'MIS?',
            'subtitle': 'Nơi khơi nguồn đa trí tuệ, nuôi dưỡng tài năng và định hình tương lai cho thế hệ công dân toàn cầu.',
            'cta_text': 'Đăng ký tư vấn',
            'cta_url': '/admissions/',
            'cta_secondary_text': 'Tham quan trường',
            'cta_secondary_url': '/contact/',
        },
        # First split section
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'GIÁO DỤC KHAI PHÓNG',
            'title': 'Phương pháp giáo dục',
            'highlight_text': 'đột phá',
            'content': '''MIS áp dụng mô hình Giáo dục Khai phóng 4.0, kết hợp tinh hoa giáo dục truyền thống với công nghệ hiện đại. Học sinh được phát triển toàn diện về kiến thức, kỹ năng và phẩm chất, sẵn sàng trở thành công dân toàn cầu trong thế kỷ 21.''',
            'cta_text': 'Tìm hiểu thêm',
            'cta_url': '/about/liberal/',
        },
        # Second split section (reversed)
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'MÔI TRƯỜNG HỌC TẬP',
            'title': 'Cơ sở vật chất',
            'highlight_text': 'hiện đại',
            'content': '''Hệ thống phòng học thông minh, thư viện đa phương tiện, phòng thí nghiệm STEAM, sân vận động tiêu chuẩn quốc tế và không gian xanh rộng lớn tạo nên môi trường học tập lý tưởng cho học sinh.''',
        },
        # Stats section
        {
            'order': 3,
            'layout': 'stats',
            'background': 'navy',
            'stat_number': '98%',
            'stat_label': 'Học sinh đạt chuẩn đầu ra',
            'title': '15+',
            'subtitle': 'Năm kinh nghiệm giáo dục',
        },
        # Third split section
        {
            'order': 4,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'ĐỘI NGŨ GIÁO VIÊN',
            'title': 'Giáo viên tận tâm,',
            'highlight_text': 'giàu kinh nghiệm',
            'content': '''Đội ngũ giáo viên MIS được tuyển chọn kỹ lưỡng, có trình độ chuyên môn cao và tâm huyết với nghề. 100% giáo viên có trình độ đại học trở lên, nhiều thầy cô có bằng thạc sĩ, tiến sĩ và chứng chỉ quốc tế.''',
        },
        # Quote section
        {
            'order': 5,
            'layout': 'quote',
            'background': 'light',
            'content': 'Giáo dục không phải là việc đổ đầy một cái bình, mà là thắp sáng một ngọn lửa. Tại MIS, chúng tôi tin rằng mỗi học sinh đều có tiềm năng vô hạn.',
            'title': 'Nhà sáng lập MIS',
        },
        # CTA section
        {
            'order': 6,
            'layout': 'cta',
            'background': 'accent',
            'eyebrow': 'SẴN SÀNG KHÁM PHÁ?',
            'title': 'Bắt đầu hành trình cùng MIS',
            'subtitle': 'Đăng ký ngay để nhận tư vấn và tham quan trường',
            'cta_text': 'Đăng ký ngay',
            'cta_url': '/admissions/',
            'cta_secondary_text': 'Liên hệ chúng tôi',
            'cta_secondary_url': '/contact/',
        },
    ]

    for data in sections_data:
        AboutSection.objects.create(page=page, **data)

    print(f'Created {len(sections_data)} sections for {page.title}')
    return True

if __name__ == '__main__':
    create_sections()
