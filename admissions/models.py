from django.db import models
from django.urls import reverse
from django.conf import settings
from core.validators import validate_upload_extension, validate_upload_file_size


def get_default_school_year():
    return getattr(settings, "MIS_PROGRAM_YEAR", "2026-2027")


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
    image = models.ImageField(upload_to='admissions/', blank=True, verbose_name="Ảnh đại diện")
    banner_image = models.ImageField(upload_to='admissions/banners/', blank=True, verbose_name="Ảnh banner")
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
    """Đơn đăng ký tuyển sinh"""
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
    
    # Thông tin phụ huynh
    parent_name = models.CharField(max_length=100, verbose_name="Họ tên phụ huynh")
    parent_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    parent_email = models.EmailField(blank=True, verbose_name="Email")
    
    # Thông tin học sinh
    student_name = models.CharField(max_length=100, verbose_name="Họ tên học sinh")
    student_dob = models.DateField(verbose_name="Ngày sinh")
    student_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Giới tính")
    current_school = models.CharField(max_length=200, blank=True, verbose_name="Trường đang học")
    current_grade = models.CharField(max_length=50, blank=True, verbose_name="Lớp hiện tại")
    
    # Thông tin liên hệ
    address = models.TextField(verbose_name="Địa chỉ")
    district = models.CharField(max_length=100, blank=True, verbose_name="Quận/Huyện")
    city = models.CharField(max_length=100, default="Hà Nội", verbose_name="Tỉnh/Thành phố")
    
    # Chương trình Phụ huynh quan tâm (checkboxes)
    interest_visit = models.BooleanField(
        default=False,
        verbose_name="Hẹn lịch tham quan trường"
    )
    interest_curriculum = models.BooleanField(
        default=False,
        verbose_name="Tư vấn chương trình học"
    )
    interest_admission_process = models.BooleanField(
        default=False,
        verbose_name="Tư vấn quy trình tuyển sinh"
    )
    
    # Thông tin bổ sung
    how_did_you_know = models.CharField(max_length=200, blank=True, verbose_name="Biết đến MIS qua")
    note = models.TextField(blank=True, verbose_name="Ghi chú")
    
    # Trạng thái
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
    file = models.FileField(
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
