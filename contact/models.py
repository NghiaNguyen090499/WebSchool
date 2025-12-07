from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
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
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False, verbose_name="Đã liên hệ")
    notes = models.TextField(blank=True, verbose_name="Ghi chú nội bộ")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Đăng ký tư vấn"
        verbose_name_plural = "Đăng ký tư vấn"
    
    def __str__(self):
        return f"{self.name} - {self.phone} - {self.get_grade_level_display()}"

