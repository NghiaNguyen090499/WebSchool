from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from core.validators import validate_upload_extension, validate_upload_file_size


def get_default_school_year():
    return getattr(settings, "MIS_PROGRAM_YEAR", "2026-2027")


# ── Choices mới cho form đăng ký ──────────────────────────────────────────

TRAINING_PROGRAM_CHOICES = [
    ('steam_chuan', 'STEAM chuẩn'),
    ('steam_clc', 'STEAM CLC'),
    ('tai_nang_toan_cn', 'Tài năng Toán - Công nghệ mới'),
    ('tai_nang_nn_en_cn', 'Tài năng ngôn ngữ Tiếng Anh & Tiếng Trung'),
    ('clc_cong_nghe', 'CLC Công nghệ (Bổ sung lớp 2-9)'),
    ('tai_nang_nn', 'Tài năng ngôn ngữ (Bổ sung lớp 3-9)'),
    ('tai_nang_toan_a', 'Tài năng Toán - Ban A (Bổ sung lớp 7 & 11)'),
    ('clc_ban_a', 'CLC - Ban A (Bổ sung Lớp 11 & 12)'),
    ('clc_ban_d', 'CLC - Ban D (Bổ sung Lớp 11 & 12)'),
    ('tai_nang_nn_d', 'Tài năng ngôn ngữ - Ban D (Bổ sung Lớp 11 & 12)'),
]

ADMISSION_METHOD_CHOICES = [
    ('xet_tuyen_thang', 'Xét tuyển thẳng'),
    ('kiem_tra_dau_vao', 'Kiểm tra đầu vào'),
    ('thi_hoc_bong', 'Thi học bổng'),
]

TARGET_GRADE_CHOICES = [
    ('mam_non', 'Mầm non'),
    ('tien_tieu_hoc', 'Tiền tiểu học'),
    ('lop_1', 'Lớp 1'),
    ('lop_2', 'Lớp 2'),
    ('lop_3', 'Lớp 3'),
    ('lop_4', 'Lớp 4'),
    ('lop_5', 'Lớp 5'),
    ('lop_6', 'Lớp 6'),
    ('lop_7', 'Lớp 7'),
    ('lop_8', 'Lớp 8'),
    ('lop_9', 'Lớp 9'),
    ('lop_10', 'Lớp 10'),
    ('lop_11', 'Lớp 11'),
    ('lop_12', 'Lớp 12'),
]

CONTACT_RELATIONSHIP_CHOICES = [
    ('bo', 'Bố'),
    ('me', 'Mẹ'),
    ('ong_ba', 'Ông/Bà'),
    ('anh_chi', 'Anh/Chị'),
    ('khac', 'Khác'),
]

SCHOOL_YEAR_CHOICES = [
    ('2026-2027', '2026-2027'),
    ('2027-2028', '2027-2028'),
]


def validate_transcript_file_size(uploaded_file):
    """Validate transcript file size: max 2MB."""
    if not uploaded_file:
        return
    max_size = 2 * 1024 * 1024  # 2MB
    if uploaded_file.size > max_size:
        raise ValidationError("File minh chứng không được vượt quá 2MB.")


def validate_transcript_extension(uploaded_file):
    """Validate transcript file: only PDF, JPG, JPEG, PNG."""
    if not uploaded_file:
        return
    import os
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    allowed = {'.pdf', '.jpg', '.jpeg', '.png'}
    if ext not in allowed:
        raise ValidationError(
            f"Chỉ chấp nhận file PDF hoặc ảnh (jpg, png). Định dạng '{ext}' không hợp lệ."
        )


class AdmissionInfo(models.Model):
    """Thông tin tuyển sinh cho từng cấp học"""
    LEVEL_CHOICES = [
        ('mam_non', 'Mầm non - Tiền tiểu học'),
        ('tieu_hoc', 'Tiểu học'),
        ('thcs', 'Trung học cơ sở'),
        ('thpt', 'Trung học phổ thông'),
    ]

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        unique=True,
        verbose_name="Cấp học"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    school_year = models.CharField(max_length=20, verbose_name="Năm học", default=get_default_school_year)
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Mô tả ngắn")
    description = models.TextField(verbose_name="Giới thiệu chung")
    age_range = models.CharField(max_length=100, blank=True, verbose_name="Độ tuổi", help_text="VD: 2-5 tuổi")
    requirements = models.TextField(verbose_name="Điều kiện tuyển sinh")
    tuition_info = models.TextField(verbose_name="Thông tin học phí")
    process = models.TextField(verbose_name="Quy trình đăng ký")
    benefits = models.TextField(blank=True, verbose_name="Ưu đãi - Học bổng")
    facilities = models.TextField(blank=True, verbose_name="Cơ sở vật chất")
    curriculum = models.TextField(blank=True, verbose_name="Chương trình học")
    deadline = models.DateField(null=True, blank=True, verbose_name="Hạn đăng ký")
    image = models.ImageField(max_length=255, upload_to='admissions/', blank=True, verbose_name="Ảnh đại diện")
    banner_image = models.ImageField(max_length=255, upload_to='admissions/banners/', blank=True, verbose_name="Ảnh banner")
    icon = models.CharField(max_length=100, default="fas fa-graduation-cap", verbose_name="Icon class")
    color = models.CharField(max_length=50, default="red", verbose_name="Màu chủ đạo", help_text="VD: red, blue, green, purple")
    is_active = models.BooleanField(default=True, verbose_name="Đang tuyển sinh")
    is_featured = models.BooleanField(default=False, verbose_name="Nổi bật")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'level']
        verbose_name = "Thông tin tuyển sinh"
        verbose_name_plural = "Thông tin tuyển sinh"

    def __str__(self):
        return f"{self.get_level_display()} - {self.school_year}"

    def get_absolute_url(self):
        return reverse('admissions:detail', kwargs={'level': self.level})


class AdmissionHighlight(models.Model):
    """Điểm nổi bật của từng cấp học"""
    admission = models.ForeignKey(AdmissionInfo, on_delete=models.CASCADE, related_name='highlights')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    description = models.TextField(verbose_name="Mô tả")
    icon = models.CharField(max_length=100, default="fas fa-check", verbose_name="Icon class")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Điểm nổi bật"
        verbose_name_plural = "Điểm nổi bật"

    def __str__(self):
        return f"{self.admission.get_level_display()} - {self.title}"


class AdmissionRegistration(models.Model):
    """Đơn đăng ký dự tuyển — mở rộng theo mẫu ANS + yêu cầu bổ sung MIS."""

    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('contacted', 'Đã liên hệ'),
        ('scheduled', 'Đã hẹn lịch'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]

    admission = models.ForeignKey(
        AdmissionInfo,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name="Cấp học đăng ký"
    )

    # ── 1. Thông tin học sinh ─────────────────────────────────────────────
    student_name = models.CharField(max_length=100, verbose_name="Họ tên học sinh")
    student_dob = models.DateField(verbose_name="Ngày sinh")
    student_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Giới tính")
    address = models.TextField(verbose_name="Nơi cư trú")
    current_school = models.CharField(max_length=200, blank=True, verbose_name="Trường đang học")
    current_grade = models.CharField(max_length=50, blank=True, verbose_name="Lớp hiện tại")

    # ── 2. Chương trình & hệ đào tạo ─────────────────────────────────────
    target_grade = models.CharField(
        max_length=30,
        choices=TARGET_GRADE_CHOICES,
        blank=True,
        verbose_name="Khối lớp dự tuyển"
    )
    training_program = models.CharField(
        max_length=30,
        choices=TRAINING_PROGRAM_CHOICES,
        blank=True,
        verbose_name="Hệ đào tạo"
    )
    registration_school_year = models.CharField(
        max_length=20,
        choices=SCHOOL_YEAR_CHOICES,
        default=get_default_school_year,
        verbose_name="Năm học đăng ký"
    )
    admission_method = models.CharField(
        max_length=30,
        choices=ADMISSION_METHOD_CHOICES,
        blank=True,
        verbose_name="Phương thức tuyển sinh"
    )
    transcript_file = models.FileField(
        upload_to='admissions/transcripts/%Y/%m/',
        blank=True,
        null=True,
        validators=[validate_transcript_extension, validate_transcript_file_size],
        verbose_name="Minh chứng xét tuyển thẳng",
        help_text="Học bạ / Phiếu điểm HK1, HK2 — scan PDF hoặc ảnh, tối đa 2 MB"
    )

    # ── 3. Thông tin bổ sung ──────────────────────────────────────────────
    study_abroad_plan = models.BooleanField(
        default=False,
        verbose_name="Dự định du học"
    )
    favorite_subjects = models.TextField(
        blank=True,
        verbose_name="Các môn học yêu thích",
        help_text="VD: Toán, Tiếng Anh, Khoa học"
    )
    best_subject = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Môn học tốt nhất"
    )
    achievements = models.TextField(
        blank=True,
        verbose_name="Thành tích đạt được",
        help_text="Ghi rõ cấp: Phường/Xã, Quận/Thành phố, Quốc gia, Quốc tế"
    )
    talent_subjects = models.TextField(
        blank=True,
        verbose_name="Môn năng khiếu đang học",
        help_text="VD: Piano, Bơi lội, Vẽ, Robotics"
    )

    # ── 4. Dịch vụ đăng ký ───────────────────────────────────────────────
    register_shuttle = models.BooleanField(
        default=False,
        verbose_name="Đăng ký xe đưa đón"
    )
    register_dayboarding = models.BooleanField(
        default=False,
        verbose_name="Đăng ký bán trú"
    )
    register_boarding = models.BooleanField(
        default=False,
        verbose_name="Đăng ký nội trú"
    )

    # ── 5. Người liên hệ ─────────────────────────────────────────────────
    parent_name = models.CharField(max_length=100, verbose_name="Họ tên người liên hệ")
    contact_relationship = models.CharField(
        max_length=20,
        choices=CONTACT_RELATIONSHIP_CHOICES,
        blank=True,
        verbose_name="Quan hệ với học sinh"
    )
    parent_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    parent_email = models.EmailField(blank=True, verbose_name="Email")
    referrer = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Người giới thiệu",
        help_text="Từ đâu anh/chị biết đến trường để đăng ký"
    )

    # ── 6. Thông tin bổ sung cũ (giữ tương thích) ────────────────────────
    district = models.CharField(max_length=100, blank=True, verbose_name="Quận/Huyện")
    city = models.CharField(max_length=100, default="Hà Nội", verbose_name="Tỉnh/Thành phố")
    interest_visit = models.BooleanField(default=False, verbose_name="Hẹn lịch tham quan trường")
    interest_curriculum = models.BooleanField(default=False, verbose_name="Tư vấn chương trình học")
    interest_admission_process = models.BooleanField(default=False, verbose_name="Tư vấn quy trình tuyển sinh")
    how_did_you_know = models.CharField(max_length=200, blank=True, verbose_name="Biết đến MIS qua")
    note = models.TextField(blank=True, verbose_name="Ghi chú")

    # ── 7. Trạng thái & nội bộ ────────────────────────────────────────────
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    admin_notes = models.TextField(blank=True, verbose_name="Ghi chú nội bộ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đơn đăng ký tuyển sinh"
        verbose_name_plural = "Đơn đăng ký tuyển sinh"

    def __str__(self):
        return f"{self.student_name} - {self.admission.get_level_display()} - {self.created_at.strftime('%d/%m/%Y')}"


class RegistrationSibling(models.Model):
    """Thông tin anh chị em ruột — inline trong đơn đăng ký."""

    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
    ]

    registration = models.ForeignKey(
        AdmissionRegistration,
        on_delete=models.CASCADE,
        related_name='siblings',
        verbose_name="Đơn đăng ký"
    )
    full_name = models.CharField(max_length=100, verbose_name="Họ tên")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Giới tính")
    current_school = models.CharField(max_length=200, verbose_name="Trường đang học")

    class Meta:
        ordering = ['id']
        verbose_name = "Anh chị em ruột"
        verbose_name_plural = "Anh chị em ruột"

    def __str__(self):
        return f"{self.full_name} ({self.registration.student_name})"


class AdmissionConsultation(models.Model):
    """Đơn đăng ký tư vấn tuyển sinh (tab 2 — form ngắn gọn)."""

    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('contacted', 'Đã liên hệ'),
        ('completed', 'Hoàn thành'),
    ]

    target_grade = models.CharField(
        max_length=30,
        choices=TARGET_GRADE_CHOICES,
        verbose_name="Tìm hiểu lớp"
    )
    training_program = models.CharField(
        max_length=30,
        choices=TRAINING_PROGRAM_CHOICES,
        blank=True,
        verbose_name="Hệ đào tạo"
    )
    details = models.TextField(
        verbose_name="Chi tiết",
        help_text="Liệt kê thông tin mà Phụ huynh mong muốn được nhận"
    )
    interest_visit = models.BooleanField(default=False, verbose_name="Hẹn lịch tham quan trường")
    interest_curriculum = models.BooleanField(default=False, verbose_name="Tư vấn chương trình học")
    interest_admission_process = models.BooleanField(default=False, verbose_name="Tư vấn quy trình tuyển sinh")
    parent_name = models.CharField(max_length=100, verbose_name="Họ tên Phụ huynh")
    phone = models.CharField(max_length=20, verbose_name="Điện thoại")
    email = models.EmailField(verbose_name="Email")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    admin_notes = models.TextField(blank=True, verbose_name="Ghi chú nội bộ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đơn tư vấn tuyển sinh"
        verbose_name_plural = "Đơn tư vấn tuyển sinh"

    def __str__(self):
        return f"{self.parent_name} - {self.get_target_grade_display()} - {self.created_at.strftime('%d/%m/%Y')}"


class AdmissionDocument(models.Model):
    """Tài liệu tuyển sinh có thể tải xuống"""
    DOCUMENT_TYPE_CHOICES = [
        ('form', 'Đơn đăng ký'),
        ('guide', 'Hướng dẫn tuyển sinh'),
        ('tuition', 'Bảng học phí'),
        ('curriculum', 'Chương trình học'),
        ('scholarship', 'Thông tin học bổng'),
        ('calendar', 'Lịch tuyển sinh'),
        ('other', 'Tài liệu khác'),
    ]

    admission = models.ForeignKey(
        AdmissionInfo,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Cấp học"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề tài liệu")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other',
        verbose_name="Loại tài liệu"
    )
    file = models.FileField(max_length=255,
        upload_to='admissions/documents/%Y/',
        validators=[validate_upload_extension, validate_upload_file_size],
        verbose_name="File tài liệu"
    )
    file_size = models.CharField(max_length=20, blank=True, verbose_name="Kích thước file")
    school_year = models.CharField(max_length=20, default=get_default_school_year, verbose_name="Năm học")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    order = models.IntegerField(default=0, verbose_name="Thứ tự hiển thị")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Số lượt tải")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Tài liệu tuyển sinh"
        verbose_name_plural = "Tài liệu tuyển sinh"

    def __str__(self):
        return f"{self.title} - {self.admission.get_level_display()} ({self.school_year})"

    def get_file_extension(self):
        """Trả về phần mở rộng của file"""
        if self.file:
            return self.file.name.split('.')[-1].upper()
        return ""

    def get_icon_class(self):
        """Trả về icon class dựa trên loại file"""
        ext = self.get_file_extension().lower()
        icons = {
            'pdf': 'fas fa-file-pdf text-red-500',
            'doc': 'fas fa-file-word text-blue-500',
            'docx': 'fas fa-file-word text-blue-500',
            'xls': 'fas fa-file-excel text-green-500',
            'xlsx': 'fas fa-file-excel text-green-500',
            'ppt': 'fas fa-file-powerpoint text-orange-500',
            'pptx': 'fas fa-file-powerpoint text-orange-500',
            'zip': 'fas fa-file-archive text-yellow-500',
            'rar': 'fas fa-file-archive text-yellow-500',
        }
        return icons.get(ext, 'fas fa-file text-neutral-500')

    def save(self, *args, **kwargs):
        # Tự động tính kích thước file
        if self.file and not self.file_size:
            size = self.file.size
            if size < 1024:
                self.file_size = f"{size} B"
            elif size < 1024 * 1024:
                self.file_size = f"{size / 1024:.1f} KB"
            else:
                self.file_size = f"{size / (1024 * 1024):.1f} MB"
        super().save(*args, **kwargs)
