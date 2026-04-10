# -*- coding: utf-8 -*-
"""
Management command để import Gương mặt nổi bật từ folder news/anh_hs
Bao gồm 4 nhóm:
1. Cuộc thi Tài năng Tin học trẻ Hà Nội 2025-2026
2. Giải Thể thao Học sinh Phổ thông Phường Cầu Giấy 2025-2026
3. TOEFL Primary Challenge - Vòng tuyển chọn cấp Thành phố
4. Vinh danh Học sinh giỏi Cụm THPT Số 3 Hà Nội 2025-2026
"""
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import StudentSpotlight


# ── 1. Cuộc thi Tài năng Tin học trẻ ──────────────────────────────────
TIN_HOC_TRE = [
    {
        'filename': 'DUONG_YEN_NHI.jpg',
        'student_name': 'Dương Yến Nhi',
        'student_class': '8A3',
        'title': 'Top 2 Cuộc thi Tài năng Tin học trẻ Hà Nội 2025-2026',
        'achievement': (
            'Xuất sắc đạt Top 2 vòng sơ loại Cuộc thi Tài năng Tin học trẻ '
            'Thành phố Hà Nội năm học 2025-2026 (cụm phường Cầu Giấy), '
            'chính thức giành vé bước vào vòng chung khảo.'
        ),
        'category': 'competition',
        'tags': 'Tin học trẻ, Top 2, Vòng chung khảo, Hà Nội',
    },
    {
        'filename': 'HY NHAT MINH.jpg',
        'student_name': 'Hy Nhật Minh',
        'student_class': '',
        'title': 'Top 5 Cuộc thi Tài năng Tin học trẻ Hà Nội 2025-2026',
        'achievement': (
            'Nỗ lực ấn tượng với thành tích Top 5 Cuộc thi Tài năng Tin học trẻ '
            'Thành phố Hà Nội năm học 2025-2026 (cụm phường Cầu Giấy), '
            'khẳng định năng lực và bản lĩnh trong sân chơi trí tuệ.'
        ),
        'category': 'competition',
        'tags': 'Tin học trẻ, Top 5, Hà Nội',
    },
]

# ── 2. Giải Thể thao HSPT Phường Cầu Giấy ───────────────────────────
THE_THAO = [
    {
        'filename': 'DAO MINH KHUE.jpg',
        'student_name': 'Đào Minh Khuê',
        'student_class': '7A3',
        'title': '2 Huy chương Vàng Bơi lội – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Xuất sắc giành 2 Huy chương Vàng (50m & 100m bơi tự do nữ) '
            'tại Giải Thể thao Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Vàng, Bơi lội, Thể thao',
    },
    {
        'filename': 'NGUYEN_THANH_VUONG.jpg',
        'student_name': 'Nguyễn Thanh Vương',
        'student_class': '8A3',
        'title': 'Huy chương Bạc Bơi lội – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Đạt Huy chương Bạc (50m bơi ếch nam) tại Giải Thể thao '
            'Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Bơi lội, Thể thao',
    },
    {
        'filename': 'CAO HAI MINH.jpg',
        'student_name': 'Cao Hải Minh',
        'student_class': '7A4',
        'title': 'Huy chương Bạc Cầu lông – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Giành Huy chương Bạc (Cầu lông đơn nam) tại Giải Thể thao '
            'Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Cầu lông, Thể thao',
    },
    {
        'filename': 'PHAM_QUANG_MINH.jpg',
        'student_name': 'Phạm Quang Minh',
        'student_class': '9A2',
        'title': 'Huy chương Bạc Cầu lông đôi – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Cùng đồng đội Vũ Nhật Anh giành Huy chương Bạc (Cầu lông đôi nam) '
            'tại Giải Thể thao Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Cầu lông đôi, Thể thao',
    },
    {
        'filename': 'VU_NHAT_ANH.jpg',
        'student_name': 'Vũ Nhật Anh',
        'student_class': '9A1',
        'title': 'Huy chương Bạc Cầu lông đôi – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Cùng đồng đội Phạm Quang Minh giành Huy chương Bạc (Cầu lông đôi nam) '
            'tại Giải Thể thao Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Cầu lông đôi, Thể thao',
    },
    {
        'filename': 'PHAM_NGUYEN_CHI_CUONG.jpg',
        'student_name': 'Phạm Nguyễn Chí Cường',
        'student_class': '8A3',
        'title': 'Huy chương Bạc Chạy 100m – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Đạt Huy chương Bạc (Chạy 100m nam) tại Giải Thể thao '
            'Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Điền kinh, Thể thao',
    },
    {
        'filename': 'DINH_HUY_YEN.jpg',
        'student_name': 'Đinh Huy Yên',
        'student_class': '9A2',
        'title': 'Huy chương Bạc Chạy 300m – Giải Thể thao HSPT Cầu Giấy',
        'achievement': (
            'Đạt Huy chương Bạc (Chạy 300m nam) tại Giải Thể thao '
            'Học sinh Phổ thông phường Cầu Giấy năm học 2025-2026.'
        ),
        'category': 'sports',
        'tags': 'Huy chương Bạc, Điền kinh, Thể thao',
    },
]

# ── 3. TOEFL Primary Challenge ────────────────────────────────────────
TOEFL_STUDENTS = [
    {
        'filename': '645619249_1343960487767050_7742366174180478950_n.jpg',
        'student_name': 'Đào Chí Hiếu',
        'student_class': '4N1',
        'title': 'TOEFL Primary Challenge – 230/230 điểm tuyệt đối',
        'achievement': (
            'Xuất sắc đạt điểm tuyệt đối 230/230 tại vòng tuyển chọn cấp Thành phố '
            'Cuộc thi TOEFL Primary Challenge do IIG Việt Nam tổ chức, '
            'sử dụng hệ thống bài thi TOEFL Primary của ETS (Hoa Kỳ). '
            'Điểm Lexile: 750L.'
        ),
        'category': 'language',
        'tags': 'TOEFL Primary, 230/230, Tiếng Anh, Tiểu học',
    },
    {
        'filename': '646693739_1343960401100392_7772028509781525628_n.jpg',
        'student_name': 'Nguyễn Hương Giang',
        'student_class': '5S2',
        'title': 'TOEFL Primary Challenge – 230/230 điểm tuyệt đối',
        'achievement': (
            'Xuất sắc đạt điểm tuyệt đối 230/230 tại vòng tuyển chọn cấp Thành phố '
            'Cuộc thi TOEFL Primary Challenge do IIG Việt Nam tổ chức, '
            'sử dụng hệ thống bài thi TOEFL Primary của ETS (Hoa Kỳ). '
            'Điểm Lexile: 750L.'
        ),
        'category': 'language',
        'tags': 'TOEFL Primary, 230/230, Tiếng Anh, Tiểu học',
    },
]

# ── 4. HSG Cụm THPT Số 3 Hà Nội 2025-2026 ───────────────────────────
# Mapped by viewing all 12 photos individually
HSG_STUDENTS = [
    {
        'filename': '665946451_1371036408392791_6938087295822611318_n.jpg',
        'student_name': 'Lê Khánh Hòa',
        'student_class': '11A5',
        'title': 'Giải Nhì Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Nhì môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Nhì, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '662689577_1371036341726131_3630303653238958071_n.jpg',
        'student_name': 'Võ Nhật Bằng',
        'student_class': '11A5',
        'title': 'Giải Nhì Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Nhì môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Nhì, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '662546999_1371036521726113_6335781787192172912_n.jpg',
        'student_name': 'Hoàng Đức Minh',
        'student_class': '11A1',
        'title': 'Giải Ba Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Ba môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Ba, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '661617026_1371036495059449_5794693803468631602_n.jpg',
        'student_name': 'Nguyễn Nhật Minh',
        'student_class': '11A2',
        'title': 'Giải Ba Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Ba môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Ba, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '662424806_1371036401726125_5178145434691541076_n.jpg',
        'student_name': 'Phạm Lê Nam Phương',
        'student_class': '11A5',
        'title': 'Giải Ba Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Ba môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Ba, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '662938810_1371036398392792_4333089968482089502_n.jpg',
        'student_name': 'Phạm Đỗ Hà An',
        'student_class': '11A5',
        'title': 'Giải Ba Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Ba môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Ba, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '666806391_1371036448392787_5348942861216235552_n.jpg',
        'student_name': 'Lê Nguyễn Thành',
        'student_class': '11A1',
        'title': 'Giải Khuyến khích Toán – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Toán tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Toán, HSG, THPT',
    },
    {
        'filename': '663142472_1371036478392784_559793049496714213_n.jpg',
        'student_name': 'Phan Hà An',
        'student_class': '11A5',
        'title': 'Giải Khuyến khích Ngữ văn – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Ngữ văn tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Ngữ văn, HSG, THPT',
    },
    {
        'filename': '665795290_1371036405059458_5598914827430675175_n.jpg',
        'student_name': 'Đặng Huyền Linh',
        'student_class': '11A3',
        'title': 'Giải Khuyến khích Ngữ văn – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Ngữ văn tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Ngữ văn, HSG, THPT',
    },
    {
        'filename': '662211404_1371036328392799_2962249290035939066_n.jpg',
        'student_name': 'Trần Ngọc Minh Khuê',
        'student_class': '10A3',
        'title': 'Giải Khuyến khích Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '667746224_1371036558392776_3383431801968190229_n.jpg',
        'student_name': 'Lại Văn Duy',
        'student_class': '10A1',
        'title': 'Giải Khuyến khích Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Tiếng Anh, HSG, THPT',
    },
    {
        'filename': '668206563_1371036538392778_3108729544170978579_n.jpg',
        'student_name': 'Nguyễn Phương Linh',
        'student_class': '10A3',
        'title': 'Giải Khuyến khích Tiếng Anh – HSG Cụm THPT Số 3 Hà Nội',
        'achievement': (
            'Đạt Giải Khuyến khích môn Tiếng Anh tại Kỳ thi Học sinh giỏi lớp 10 & 11 – '
            'Cụm trường THPT số 3, TP. Hà Nội năm học 2025-2026.'
        ),
        'category': 'academic',
        'tags': 'Giải Khuyến khích, Tiếng Anh, HSG, THPT',
    },
]

# ── Folder mapping ────────────────────────────────────────────────────
GROUPS = [
    {
        'label': 'Tài năng Tin học trẻ Hà Nội 2025-2026',
        'folder': 'CUỘC THI TÀI NĂNG TIN HỌC TRẺ HÀ NỘI 2025 – 2026',
        'students': TIN_HOC_TRE,
    },
    {
        'label': 'Giải Thể thao HSPT Cầu Giấy 2025-2026',
        'folder': 'GIẢI THỂ THAO HỌC SINH PHỔ THÔNG PHƯỜNG CẦU GIẤY 2025 – 2026',
        'students': THE_THAO,
    },
    {
        'label': 'TOEFL Primary Challenge',
        'folder': 'MISERS GHI DẤU ẤN TẠI VÒNG TUYỂN CHỌN CẤP THÀNH PHỐ CUỘC THI TOEFL PRIMARY CHALLENGE',
        'students': TOEFL_STUDENTS,
    },
    {
        'label': 'HSG Cụm THPT Số 3 Hà Nội 2025-2026',
        'folder': 'VINH DANH HỌC SINH MIS ĐẠT THÀNH TÍCH CAO – KỲ THI HỌC SINH GIỎI CỤM THPT SỐ 3 HÀ NỘI 2025–2026',
        'students': HSG_STUDENTS,
    },
]


class Command(BaseCommand):
    help = 'Import Guong mat noi bat 2025-2026 from news/anh_hs'

    def add_arguments(self, parser):
        from django.conf import settings
        parser.add_argument(
            '--source',
            type=str,
            default=os.path.join(settings.BASE_DIR, 'news', 'anh_hs'),
            help='Path to folder containing photos (default: news/anh_hs)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview only, do not actually import',
        )

    def _safe_print(self, msg, style_func=None):
        """Print with fallback for Windows console encoding issues."""
        try:
            if style_func:
                self.stdout.write(style_func(msg))
            else:
                self.stdout.write(msg)
        except UnicodeEncodeError:
            safe = msg.encode('ascii', errors='replace').decode('ascii')
            if style_func:
                self.stdout.write(style_func(safe))
            else:
                self.stdout.write(safe)

    def handle(self, *args, **options):
        source_dir = options['source']
        dry_run = options['dry_run']

        if not os.path.exists(source_dir):
            self.stderr.write(self.style.ERROR(f'Folder not found: {source_dir}'))
            return

        self._safe_print(f'Import Student Spotlight from: {source_dir}', self.style.MIGRATE_HEADING)

        # Determine starting order based on existing records
        max_order = StudentSpotlight.objects.order_by('-order').values_list('order', flat=True).first() or 0
        global_order = max_order + 1

        total_created = 0
        total_skipped = 0

        for group in GROUPS:
            folder_path = os.path.join(source_dir, group['folder'])
            self._safe_print(f'\n{"="*60}')
            self._safe_print(f'  {group["label"]}', self.style.MIGRATE_HEADING)
            self._safe_print(f'  Folder: {group["folder"]}')

            if not os.path.exists(folder_path):
                self._safe_print('  [!] Folder not found, skipping', self.style.WARNING)
                continue

            for student_data in group['students']:
                created, skipped = self._import_student(
                    student_data, folder_path, global_order, dry_run,
                )
                total_created += created
                total_skipped += skipped
                if created:
                    global_order += 1

        self._safe_print(f'\n{"="*60}')
        if dry_run:
            self._safe_print(
                f'[DRY RUN] Would create {total_created} records, skipped {total_skipped}',
                self.style.WARNING,
            )
        else:
            self._safe_print(
                f'[DONE] Imported {total_created} students, skipped {total_skipped}',
                self.style.SUCCESS,
            )

    def _import_student(self, student_data, folder, order, dry_run):
        filename = student_data['filename']
        filepath = os.path.join(folder, filename)

        if not os.path.exists(filepath):
            self._safe_print(f'  [!] Not found: {filename}', self.style.WARNING)
            return 0, 1

        student_name = student_data['student_name']

        # Check if already exists
        existing = StudentSpotlight.objects.filter(
            student_name=student_name,
            title=student_data['title'],
        ).first()
        if existing:
            self._safe_print(f'  [~] {student_name} -- already exists, skipping')
            return 0, 1

        self._safe_print(f'  [+] {student_name} ({student_data.get("student_class", "")}) -- {filename}')

        if dry_run:
            return 1, 0

        spotlight = StudentSpotlight(
            student_name=student_name,
            student_class=student_data.get('student_class', ''),
            title=student_data['title'],
            achievement=student_data['achievement'],
            category=student_data['category'],
            tags=student_data.get('tags', ''),
            is_featured=True,
            is_active=True,
            order=order,
        )

        with open(filepath, 'rb') as f:
            spotlight.photo.save(filename, File(f), save=False)

        spotlight.save()
        self._safe_print(f'      -> Created OK (order={order})', self.style.SUCCESS)
        return 1, 0

