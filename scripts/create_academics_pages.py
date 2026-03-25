# -*- coding: utf-8 -*-
"""
Script to create Academics pages with Nord Anglia style sections
Vietnamese content with proper accents
Run with: python scripts/create_academics_pages.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from about.models import AboutPage, AboutSection

def create_academics_overview():
    """Create main Academics overview page"""
    page, created = AboutPage.objects.get_or_create(
        page_type='academics',
        defaults={'title': 'Tổng quan Chương trình Giáo dục', 'content': ''}
    )
    if not created:
        page.title = 'Tổng quan Chương trình Giáo dục'
        page.save()
    page.sections.all().delete()
    
    sections = [
        # Hero
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'CHƯƠNG TRÌNH HỌC',
            'title': 'TỔNG QUAN CHƯƠNG TRÌNH',
            'highlight_text': 'GIÁO DỤC',
            'subtitle': 'Hệ thống giáo dục Đa Trí Tuệ - MIS tiên phong xây dựng chương trình giáo dục toàn diện, kết hợp chuẩn quốc gia với phương pháp hiện đại, lấy phát triển đa trí tuệ làm trọng tâm.',
            'cta_text': 'Liên hệ tư vấn',
            'cta_url': '/admissions/',
        },
        # Preschool
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'MẦM NON (3-6 TUỔI)',
            'title': 'Ươm Mầm Tư Duy',
            'highlight_text': 'Và Cảm Xúc',
            'content': '''Chương trình giáo dục phát triển toàn diện "Thể chất – Trí tuệ - Cảm xúc".

• Áp dụng phương pháp "Hands on learning", tập trung phát triển ngôn ngữ, tư duy logic, kỹ năng xã hội
• Môi trường giáo dục song ngữ: 50% Tiếng Anh, 50% Tiếng Việt
• Tạo nền tảng vững vàng về tri thức, kỹ năng và an toàn về cảm xúc trước khi bước vào Lớp 1''',
            'cta_text': 'Tìm hiểu thêm',
            'cta_url': '/about/academics/preschool/',
        },
        # Primary
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'TIỂU HỌC (LỚP 1-5)',
            'title': 'Khám Phá & Khơi Mở',
            'highlight_text': 'Tiềm Năng',
            'content': '''Bám sát chương trình của Bộ GD&ĐT, tích hợp STEM/STEAM, dự án liên môn và giáo dục cá nhân hóa.

• Chú trọng rèn luyện tư duy phản biện, năng lực số và tiếng Anh (theo chuẩn Cambridge)
• Tập trung khám phá, khơi mở các tiềm năng đa trí tuệ và định hình nhân cách
• Làm quen ngoại ngữ 2: Tiếng Trung''',
            'cta_text': 'Tìm hiểu thêm',
            'cta_url': '/about/academics/primary/',
        },
        # Stats
        {
            'order': 3,
            'layout': 'stats',
            'background': 'navy',
            'stat_number': '4',
            'stat_label': 'Cấp học liên thông',
            'title': '8',
            'subtitle': 'Loại hình trí thông minh',
        },
        # Middle School
        {
            'order': 4,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'THCS (LỚP 6-9)',
            'title': 'Định Hình Tư Duy',
            'highlight_text': 'Toàn Diện',
            'content': '''Tăng cường giáo dục định hướng, phương pháp "Học qua trải nghiệm" kết hợp STEAM.

• Phát triển kỹ năng sống, giá trị sống và năng lực cảm xúc xã hội
• Đẩy mạnh nghiên cứu khoa học, trải nghiệm thực tế
• Song ngữ Anh-Việt: chuẩn đầu ra Cambridge và luyện thi IELTS từ lớp 6
• CLB chuyên sâu: Robotics, Toán học ứng dụng, Debate, Thiết kế AI''',
            'cta_text': 'Tìm hiểu thêm',
            'cta_url': '/about/academics/middle/',
        },
        # High School
        {
            'order': 5,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'THPT (LỚP 10-12)',
            'title': 'Bứt Phá',
            'highlight_text': 'Đỉnh Cao',
            'content': '''Lộ trình đa dạng: Công nghệ Quốc tế (liên kết Aptech), HSK5+ (Trung Quốc), Tài năng Toán học & Tiếng Anh.

• Định hướng nghề nghiệp qua lộ trình cá nhân hóa
• Hướng nghiệp 4.0: Thực tập tại doanh nghiệp công nghệ
• Định hướng du học hoặc thi đại học với các chứng chỉ quốc tế
• Định hình rõ "con đường nhân cách" hướng tới tương lai hạnh phúc bền vững''',
            'cta_text': 'Tìm hiểu thêm',
            'cta_url': '/about/academics/high/',
        },
        # CTA
        {
            'order': 6,
            'layout': 'cta',
            'background': 'accent',
            'eyebrow': 'SẴN SÀNG BẮT ĐẦU?',
            'title': 'Đăng ký tư vấn ngay',
            'subtitle': 'Để được tư vấn chi tiết về chương trình phù hợp với con bạn',
            'cta_text': 'Đăng ký ngay',
            'cta_url': '/admissions/',
            'cta_secondary_text': 'Tham quan trường',
            'cta_secondary_url': '/contact/',
        },
    ]
    
    for data in sections:
        AboutSection.objects.create(page=page, **data)
    
    print(f'Created {len(sections)} sections for Academics Overview')


def create_preschool_page():
    """Create Preschool (Mầm non) page"""
    page, created = AboutPage.objects.get_or_create(
        page_type='preschool',
        defaults={'title': 'Chương trình Mầm non (3-6 tuổi)', 'content': ''}
    )
    if not created:
        page.title = 'Chương trình Mầm non (3-6 tuổi)'
        page.save()
    page.sections.all().delete()
    
    sections = [
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'MẦM NON (3-6 TUỔI)',
            'title': 'ƯƠM MẦM TƯ DUY',
            'highlight_text': 'VÀ CẢM XÚC',
            'subtitle': 'Chương trình giáo dục phát triển toàn diện "Thể chất – Trí tuệ - Cảm xúc" dành cho trẻ từ 3-6 tuổi.',
        },
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'PHƯƠNG PHÁP',
            'title': 'Học Qua',
            'highlight_text': 'Trải Nghiệm',
            'content': '''Áp dụng phương pháp "Hands on learning" - học qua làm, tập trung phát triển:

• Ngôn ngữ và giao tiếp
• Tư duy logic và sáng tạo
• Kỹ năng xã hội và cảm xúc
• Khơi dậy tiềm năng qua trải nghiệm đa giác quan''',
        },
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'SONG NGỮ',
            'title': 'Môi Trường',
            'highlight_text': 'Song Ngữ',
            'content': '''Môi trường giáo dục song ngữ cân bằng:

• 50% hoạt động giáo dục bằng Tiếng Anh
• 50% hoạt động giáo dục bằng Tiếng Việt
• Giáo viên bản ngữ và giáo viên Việt Nam có chứng chỉ quốc tế
• Tạo nền tảng ngôn ngữ vững chắc từ nhỏ''',
        },
        {
            'order': 3,
            'layout': 'cta',
            'background': 'accent',
            'title': 'Đăng ký tham quan trường',
            'cta_text': 'Đăng ký ngay',
            'cta_url': '/admissions/',
        },
    ]
    
    for data in sections:
        AboutSection.objects.create(page=page, **data)
    
    print(f'Created {len(sections)} sections for Preschool page')


def create_primary_page():
    """Create Primary (Tiểu học) page"""
    page, created = AboutPage.objects.get_or_create(
        page_type='primary',
        defaults={'title': 'Chương trình Tiểu học (Lớp 1-5)', 'content': ''}
    )
    if not created:
        page.title = 'Chương trình Tiểu học (Lớp 1-5)'
        page.save()
    page.sections.all().delete()
    
    sections = [
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'TIỂU HỌC (LỚP 1-5)',
            'title': 'KHÁM PHÁ & KHƠI MỞ',
            'highlight_text': 'TIỀM NĂNG',
            'subtitle': 'Bám sát chương trình Bộ GD&ĐT, tích hợp STEM/STEAM và giáo dục cá nhân hóa.',
        },
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'ĐIỂM KHÁC BIỆT',
            'title': 'Giáo Dục',
            'highlight_text': 'Toàn Diện',
            'content': '''Chương trình Tiểu học MIS tập trung:

• Rèn luyện tư duy phản biện và sáng tạo
• Phát triển năng lực số và công nghệ
• Tiếng Anh theo chuẩn Cambridge
• Tích hợp dự án liên môn STEAM''',
        },
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'NGOẠI NGỮ',
            'title': 'Đa Ngôn Ngữ',
            'highlight_text': 'Từ Nhỏ',
            'content': '''Chương trình ngoại ngữ mạnh mẽ:

• Tiếng Anh: theo chuẩn Cambridge, học với giáo viên bản ngữ
• Tiếng Trung: làm quen từ lớp 3, phát triển tư duy đa văn hóa
• Kỹ năng giao tiếp quốc tế''',
        },
        {
            'order': 3,
            'layout': 'cta',
            'background': 'accent',
            'title': 'Tìm hiểu thêm về chương trình',
            'cta_text': 'Liên hệ tư vấn',
            'cta_url': '/admissions/',
        },
    ]
    
    for data in sections:
        AboutSection.objects.create(page=page, **data)
    
    print(f'Created {len(sections)} sections for Primary page')


def create_middle_page():
    """Create Middle School (THCS) page"""
    page, created = AboutPage.objects.get_or_create(
        page_type='middle',
        defaults={'title': 'Chương trình THCS (Lớp 6-9)', 'content': ''}
    )
    if not created:
        page.title = 'Chương trình THCS (Lớp 6-9)'
        page.save()
    page.sections.all().delete()
    
    sections = [
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'THCS (LỚP 6-9)',
            'title': 'ĐỊNH HÌNH TƯ DUY',
            'highlight_text': 'TOÀN DIỆN',
            'subtitle': 'Phương pháp "Học qua trải nghiệm" kết hợp STEAM, giúp học sinh phát triển toàn diện 8 loại hình trí thông minh.',
        },
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'CHƯƠNG TRÌNH CHÍNH',
            'title': 'Học Tập',
            'highlight_text': 'Toàn Diện',
            'content': '''Chương trình THCS MIS bao gồm:

• Tăng cường giáo dục định hướng nghề nghiệp
• Phát triển kỹ năng sống và giá trị sống
• Đẩy mạnh nghiên cứu khoa học, trải nghiệm thực tế
• Năng lực cảm xúc xã hội (SEL)''',
        },
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'NGOẠI NGỮ',
            'title': 'Song Ngữ',
            'highlight_text': 'Anh-Việt',
            'content': '''Chương trình ngoại ngữ mạnh:

• Chuẩn đầu ra Cambridge cho THCS
• Luyện thi IELTS từ lớp 6
• Phát triển Tiếng Trung làm ngoại ngữ 2
• Cơ hội trao đổi học sinh quốc tế''',
        },
        {
            'order': 3,
            'layout': 'full_text',
            'background': 'white',
            'eyebrow': 'CLB CHUYÊN SÂU',
            'title': 'Câu lạc bộ',
            'content': '''• Robotics - Thiết kế và lập trình robot
• Toán học ứng dụng - Phát triển tư duy logic
• Debate - Rèn luyện kỹ năng tranh biện
• Thiết kế AI - Làm quen trí tuệ nhân tạo''',
        },
        {
            'order': 4,
            'layout': 'cta',
            'background': 'accent',
            'title': 'Đăng ký học thử',
            'cta_text': 'Đăng ký ngay',
            'cta_url': '/admissions/',
        },
    ]
    
    for data in sections:
        AboutSection.objects.create(page=page, **data)
    
    print(f'Created {len(sections)} sections for Middle School page')


def create_high_page():
    """Create High School (THPT) page"""
    page, created = AboutPage.objects.get_or_create(
        page_type='high',
        defaults={'title': 'Chương trình THPT (Lớp 10-12)', 'content': ''}
    )
    if not created:
        page.title = 'Chương trình THPT (Lớp 10-12)'
        page.save()
    page.sections.all().delete()
    
    sections = [
        {
            'order': 0,
            'layout': 'hero',
            'background': 'navy',
            'eyebrow': 'THPT (LỚP 10-12)',
            'title': 'BỨT PHÁ',
            'highlight_text': 'ĐỈNH CAO',
            'subtitle': 'Lộ trình đa dạng: Công nghệ Quốc tế, HSK5+, Tài năng Toán học & Tiếng Anh.',
        },
        {
            'order': 1,
            'layout': 'text_left',
            'background': 'white',
            'eyebrow': 'LỘ TRÌNH ĐA DẠNG',
            'title': 'Chương Trình',
            'highlight_text': 'Liên Kết',
            'content': '''Nhiều lựa chọn lộ trình:

• Công nghệ Quốc tế: liên kết Aptech, Chứng chỉ công nhận toàn cầu
• HSK5+: Chương trình Tiếng Trung chuyên sâu cho du học Trung Quốc
• Tài năng Toán học: Luyện thi Olympic và đại học top
• Tài năng Tiếng Anh: IELTS 7.0+ và du học''',
        },
        {
            'order': 2,
            'layout': 'text_right',
            'background': 'light',
            'eyebrow': 'HƯỚNG NGHIỆP 4.0',
            'title': 'Định Hướng',
            'highlight_text': 'Nghề Nghiệp',
            'content': '''Chương trình hướng nghiệp toàn diện:

• Thực tập tại doanh nghiệp công nghệ
• Định hướng du học hoặc thi đại học
• Lấy các chứng chỉ quốc tế (IELTS, SAT, HSK...)
• Tư vấn lộ trình cá nhân hóa''',
        },
        {
            'order': 3,
            'layout': 'quote',
            'background': 'light',
            'content': 'Định hình rõ "con đường nhân cách" hướng tới tương lai hạnh phúc bền vững.',
            'title': 'Triết lý giáo dục MIS',
        },
        {
            'order': 4,
            'layout': 'cta',
            'background': 'accent',
            'title': 'Sẵn sàng cho tương lai?',
            'cta_text': 'Đăng ký tư vấn',
            'cta_url': '/admissions/',
            'cta_secondary_text': 'Tham quan trường',
            'cta_secondary_url': '/contact/',
        },
    ]
    
    for data in sections:
        AboutSection.objects.create(page=page, **data)
    
    print(f'Created {len(sections)} sections for High School page')


if __name__ == '__main__':
    create_academics_overview()
    create_preschool_page()
    create_primary_page()
    create_middle_page()
    create_high_page()
    print('\nAll Academics pages created successfully!')
