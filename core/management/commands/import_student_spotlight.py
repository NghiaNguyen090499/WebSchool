# -*- coding: utf-8 -*-
"""
Management command để import Student Spotlight từ folder ảnh
"""
import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from core.models import StudentSpotlight


class Command(BaseCommand):
    help = 'Import Student Spotlight từ folder ảnh'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default=r'D:\NGHIA\WebsiteSchool\WEBSITE 2026 MIS&ARAR\vinh danh',
            help='Đường dẫn đến folder chứa ảnh'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Chỉ hiển thị, không import thực sự'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Xóa tất cả StudentSpotlight hiện có trước khi import'
        )

    def handle(self, *args, **options):
        source_dir = options['source']
        dry_run = options['dry_run']
        clear = options['clear']

        if not os.path.exists(source_dir):
            self.stderr.write(self.style.ERROR(f'Folder không tồn tại: {source_dir}'))
            return

        if clear and not dry_run:
            deleted_count = StudentSpotlight.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f'Đã xóa {deleted_count} records cũ'))

        # Định nghĩa data cho học sinh ASMO
        asmo_students = [
            {
                'filename': 'dang khoi.png',
                'student_name': 'Đặng Khôi',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Đạt thành tích xuất sắc tại vòng Quốc gia cuộc thi Olympic Toán học và Khoa học ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'diep chi.png',
                'student_name': 'Diệp Chi',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Xuất sắc giành huy chương tại cuộc thi Olympic Toán học và Khoa học ASMO 2025 vòng Quốc gia.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'duc anh.png',
                'student_name': 'Đức Anh',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Thể hiện năng lực Toán học vượt trội, đạt huy chương tại ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'hai minh.png',
                'student_name': 'Hải Minh',
                'student_class': 'Khối Tiểu học',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Đạt giải thưởng xuất sắc tại cuộc thi ASMO 2025 vòng Quốc gia.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'huy bao.png',
                'student_name': 'Huy Bảo',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Vinh dự nhận huy chương tại cuộc thi Olympic Toán học ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'khoi nguyen.png',
                'student_name': 'Khôi Nguyên',
                'student_class': 'Khối Tiểu học',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Xuất sắc đạt giải tại cuộc thi ASMO 2025 - Olympic Toán học và Khoa học châu Á.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'linh thao.png',
                'student_name': 'Linh Thảo',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Đạt huy chương tại vòng Quốc gia cuộc thi ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'minh quan.png',
                'student_name': 'Minh Quân',
                'student_class': 'Khối Tiểu học',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Thể hiện tư duy Toán học xuất sắc, đạt giải tại ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'minh son.png',
                'student_name': 'Minh Sơn',
                'student_class': 'Khối Tiểu học',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Vinh dự đạt huy chương tại cuộc thi Olympic ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'ngan an.png',
                'student_name': 'Ngân An',
                'student_class': 'Khối Tiểu học',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Xuất sắc giành giải thưởng tại cuộc thi ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, Vòng Quốc gia',
            },
            {
                'filename': 'quang anh.png',
                'student_name': 'Quang Anh',
                'student_class': 'Khối THCS',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Đạt thành tích cao tại vòng Quốc gia cuộc thi ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, THCS, Vòng Quốc gia',
            },
            {
                'filename': 'vd linh giang.png',
                'student_name': 'Linh Giang',
                'student_class': 'Khối THCS',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Xuất sắc đạt huy chương tại cuộc thi Olympic ASMO 2025 vòng Quốc gia.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, THCS, Vòng Quốc gia',
            },
            {
                'filename': 'vu anh.png',
                'student_name': 'Vũ Anh',
                'student_class': 'Khối THCS',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Thể hiện năng lực vượt trội, đạt giải tại ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, THCS, Vòng Quốc gia',
            },
            {
                'filename': 'Hoang nguyen.png',
                'student_name': 'Hoàng Nguyên',
                'student_class': 'Khối THPT',
                'title': 'Huy chương ASMO 2025',
                'achievement': 'Đạt huy chương xuất sắc tại cuộc thi ASMO 2025 vòng Quốc gia.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, THPT, Vòng Quốc gia',
            },
            {
                'filename': 'tran quang.png',
                'student_name': 'Trần Quang',
                'student_class': 'Khối THPT',
                'title': 'Giải thưởng ASMO 2025',
                'achievement': 'Vinh dự đạt giải thưởng tại cuộc thi Olympic ASMO 2025.',
                'category': 'competition',
                'tags': 'ASMO, Toán học, THPT, Vòng Quốc gia',
            },
        ]

        # Thêm học sinh từ folder gốc (vinh danh)
        root_students = [
            {
                'filename': 'ba nguyen.png',
                'student_name': 'Bá Nguyên',
                'student_class': 'Khối THPT',
                'title': 'Học sinh xuất sắc',
                'achievement': 'Gương mặt học sinh tiêu biểu của MIS với thành tích học tập và hoạt động ngoại khóa xuất sắc.',
                'category': 'academic',
                'tags': 'Học sinh xuất sắc, THPT',
            },
            {
                'filename': 'bao ngoc.png',
                'student_name': 'Bảo Ngọc',
                'student_class': 'Khối THCS',
                'title': 'Học sinh tiêu biểu',
                'achievement': 'Vinh danh học sinh có thành tích học tập và rèn luyện đạo đức xuất sắc.',
                'category': 'academic',
                'tags': 'Học sinh tiêu biểu, THCS',
            },
            {
                'filename': 'hong nam.png',
                'student_name': 'Hồng Nam',
                'student_class': 'Khối THCS',
                'title': 'Gương mặt MISers',
                'achievement': 'Học sinh nổi bật với tinh thần học hỏi và sáng tạo trong các hoạt động.',
                'category': 'academic',
                'tags': 'Gương mặt MISers, THCS',
            },
            {
                'filename': 'lam phong.png',
                'student_name': 'Lâm Phong',
                'student_class': 'Khối THPT',
                'title': 'Học sinh ưu tú',
                'achievement': 'Đại diện tiêu biểu cho thế hệ MISers với thành tích học tập đáng ngưỡng mộ.',
                'category': 'academic',
                'tags': 'Học sinh ưu tú, THPT',
            },
            {
                'filename': 'my cam.png',
                'student_name': 'Mỹ Cầm',
                'student_class': 'Khối THPT',
                'title': 'Học sinh xuất sắc toàn diện',
                'achievement': 'Nổi bật trong cả học tập và các hoạt động văn nghệ, thể thao.',
                'category': 'academic',
                'tags': 'Học sinh xuất sắc, THPT, Toàn diện',
            },
            {
                'filename': 'nam anh.png',
                'student_name': 'Nam Anh',
                'student_class': 'Khối THCS',
                'title': 'Gương mặt tiêu biểu',
                'achievement': 'Học sinh có tinh thần trách nhiệm cao và kết quả học tập ấn tượng.',
                'category': 'academic',
                'tags': 'Gương mặt tiêu biểu, THCS',
            },
            {
                'filename': 'phuc lam.png',
                'student_name': 'Phúc Lâm',
                'student_class': 'Khối Tiểu học',
                'title': 'Học sinh gương mẫu',
                'achievement': 'Bé ngoan, học giỏi và tích cực tham gia các hoạt động của trường.',
                'category': 'academic',
                'tags': 'Học sinh gương mẫu, Tiểu học',
            },
        ]

        created_count = 0
        skipped_count = 0

        # Import ASMO students
        asmo_folder = os.path.join(source_dir, 'ASMO')
        if os.path.exists(asmo_folder):
            self.stdout.write(f'\n[ASMO] Dang xu ly folder ASMO...')
            for i, student_data in enumerate(asmo_students):
                created, skipped = self._import_student(
                    student_data, asmo_folder, i, dry_run, is_featured=(i < 6)
                )
                created_count += created
                skipped_count += skipped

        # Import root students
        self.stdout.write(f'\n[ROOT] Dang xu ly folder goc...')
        for i, student_data in enumerate(root_students):
            created, skipped = self._import_student(
                student_data, source_dir, i + len(asmo_students), dry_run, is_featured=(i < 4)
            )
            created_count += created
            skipped_count += skipped

        self.stdout.write('')
        if dry_run:
            self.stdout.write(self.style.WARNING(f'[DRY RUN] Se tao {created_count} records, bo qua {skipped_count}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'[OK] Da import {created_count} hoc sinh, bo qua {skipped_count}'))

    def _import_student(self, student_data, folder, order, dry_run, is_featured=False):
        filename = student_data['filename']
        filepath = os.path.join(folder, filename)

        if not os.path.exists(filepath):
            self.stdout.write(self.style.WARNING(f'  [!] Khong tim thay: {filename}'))
            return 0, 1

        self.stdout.write(f'  [+] {filename}')

        if dry_run:
            return 1, 0

        # Check if already exists
        existing = StudentSpotlight.objects.filter(student_name=student_data['student_name']).first()
        if existing:
            self.stdout.write(self.style.WARNING(f'      -> Da ton tai, bo qua'))
            return 0, 1

        # Create new record
        spotlight = StudentSpotlight(
            student_name=student_data['student_name'],
            student_class=student_data['student_class'],
            title=student_data['title'],
            achievement=student_data['achievement'],
            category=student_data['category'],
            tags=student_data['tags'],
            is_featured=is_featured,
            is_active=True,
            order=order,
        )

        # Save photo
        with open(filepath, 'rb') as f:
            spotlight.photo.save(filename, File(f), save=False)

        spotlight.save()
        self.stdout.write(self.style.SUCCESS(f'      -> Da tao thanh cong'))
        return 1, 0
