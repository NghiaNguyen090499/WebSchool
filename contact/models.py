from django.db import models


class ContactMessage(models.Model):
    GRADE_CHOICES = [
        ('', 'Chưa chọn'),
        ('mam_non', 'Mầm non - Tiền tiểu học'),
        ('tieu_hoc', 'Tiểu học (Lớp 1-5)'),
        ('thcs', 'THCS (Lớp 6-9)'),
        ('thpt', 'THPT (Lớp 10-12)'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    grade_level = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        blank=True,
        default='',
        verbose_name="Cấp học quan tâm"
    )
    message = models.TextField()
    
    # Chương trình Phụ huynh quan tâm (đồng bộ với AdmissionRegistration & ConsultationRequest)
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class ConsultationRequest(models.Model):
    GRADE_CHOICES = [
        ('mam_non', 'Mầm non - Tiền tiểu học'),
        ('tieu_hoc', 'Tiểu học (Lớp 1-5)'),
        ('thcs', 'THCS (Lớp 6-9)'),
        ('thpt', 'THPT (Lớp 10-12)'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Họ tên phụ huynh")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    grade_level = models.CharField(max_length=20, choices=GRADE_CHOICES, verbose_name="Cấp học quan tâm")
    message = models.TextField(blank=True, verbose_name="Nội dung cần tư vấn")
    
    # Chương trình Phụ huynh quan tâm (checkboxes - đồng bộ với AdmissionRegistration)
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False, verbose_name="Đã liên hệ")
    notes = models.TextField(blank=True, verbose_name="Ghi chú nội bộ")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đăng ký tư vấn"
        verbose_name_plural = "Đăng ký tư vấn"
    
    def __str__(self):
        return f"{self.name} - {self.phone} - {self.get_grade_level_display()}"


class ChatbotLead(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.phone}"
