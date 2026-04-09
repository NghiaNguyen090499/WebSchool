from django.contrib import admin
from .models import (
    AdmissionInfo,
    AdmissionHighlight,
    AdmissionRegistration,
    RegistrationSibling,
    AdmissionConsultation,
    AdmissionDocument,
)


class AdmissionHighlightInline(admin.TabularInline):
    model = AdmissionHighlight
    extra = 1
    fields = ['title', 'description', 'icon', 'order']


class AdmissionDocumentInline(admin.TabularInline):
    model = AdmissionDocument
    extra = 1
    fields = ['title', 'document_type', 'file', 'school_year', 'is_active', 'order']
    readonly_fields = ['download_count']


class RegistrationSiblingInline(admin.TabularInline):
    model = RegistrationSibling
    extra = 0
    fields = ['full_name', 'date_of_birth', 'gender', 'current_school']


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['level', 'title', 'school_year', 'is_active', 'is_featured', 'order', 'updated_at']
    list_filter = ['is_active', 'is_featured', 'school_year']
    list_editable = ['is_active', 'is_featured', 'order']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AdmissionHighlightInline, AdmissionDocumentInline]

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('level', 'title', 'school_year', 'subtitle', 'age_range')
        }),
        ('Nội dung', {
            'fields': ('description', 'requirements', 'tuition_info', 'process', 'benefits', 'facilities', 'curriculum')
        }),
        ('Hình ảnh & Giao diện', {
            'fields': ('image', 'banner_image', 'icon', 'color')
        }),
        ('Cài đặt', {
            'fields': ('deadline', 'is_active', 'is_featured', 'order')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdmissionRegistration)
class AdmissionRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'admission', 'target_grade', 'training_program',
        'admission_method', 'parent_name', 'parent_phone', 'status', 'created_at',
    ]
    list_filter = [
        'status', 'admission', 'target_grade', 'training_program',
        'admission_method', 'registration_school_year',
        'study_abroad_plan', 'register_shuttle', 'register_dayboarding', 'register_boarding',
        'created_at', 'student_gender',
    ]
    list_editable = ['status']
    search_fields = ['student_name', 'parent_name', 'parent_phone', 'parent_email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [RegistrationSiblingInline]

    fieldsets = (
        ('Cấp học & Trạng thái', {
            'fields': ('admission', 'status')
        }),
        ('1. Thông tin học sinh', {
            'fields': (
                'student_name', 'student_dob', 'student_gender',
                'address', 'current_school', 'current_grade',
            )
        }),
        ('2. Chương trình & Hệ đào tạo', {
            'fields': (
                'target_grade', 'training_program',
                'registration_school_year', 'admission_method',
                'transcript_file',
            )
        }),
        ('3. Thông tin bổ sung', {
            'fields': (
                'study_abroad_plan', 'study_abroad_country',
                'favorite_subjects', 'best_subject',
                'achievements', 'talent_subjects',
            )
        }),
        ('4. Dịch vụ đăng ký', {
            'fields': (
                'register_shuttle', 'register_dayboarding', 'register_boarding',
            )
        }),
        ('5. Người liên hệ', {
            'fields': (
                'parent_name', 'contact_relationship',
                'parent_phone', 'parent_email',
                'referrer',
            )
        }),
        ('6. Thông tin khác', {
            'fields': ('district', 'city', 'how_did_you_know', 'note'),
            'classes': ('collapse',)
        }),
        ('7. Quan tâm (cũ)', {
            'fields': ('interest_visit', 'interest_curriculum', 'interest_admission_process'),
            'classes': ('collapse',)
        }),
        ('Ghi chú nội bộ', {
            'fields': ('admin_notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_contacted', 'mark_as_scheduled', 'mark_as_approved']

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
        self.message_user(request, f"Đã cập nhật {queryset.count()} đơn thành 'Đã liên hệ'")
    mark_as_contacted.short_description = "Đánh dấu đã liên hệ"

    def mark_as_scheduled(self, request, queryset):
        queryset.update(status='scheduled')
        self.message_user(request, f"Đã cập nhật {queryset.count()} đơn thành 'Đã hẹn lịch'")
    mark_as_scheduled.short_description = "Đánh dấu đã hẹn lịch"

    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"Đã cập nhật {queryset.count()} đơn thành 'Đã duyệt'")
    mark_as_approved.short_description = "Đánh dấu đã duyệt"


@admin.register(AdmissionConsultation)
class AdmissionConsultationAdmin(admin.ModelAdmin):
    list_display = [
        'parent_name', 'target_grade', 'training_program',
        'phone', 'email', 'status', 'created_at',
    ]
    list_filter = ['status', 'target_grade', 'training_program', 'created_at']
    list_editable = ['status']
    search_fields = ['parent_name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Thông tin tìm hiểu', {
            'fields': (
                'target_grade', 'training_program', 'details',
                'interest_visit', 'interest_curriculum', 'interest_admission_process',
            )
        }),
        ('Thông tin phụ huynh', {
            'fields': ('parent_name', 'phone', 'email')
        }),
        ('Trạng thái', {
            'fields': ('status', 'admin_notes')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_contacted', 'mark_as_completed']

    def mark_as_contacted(self, request, queryset):
        queryset.update(status='contacted')
        self.message_user(request, f"Đã cập nhật {queryset.count()} đơn thành 'Đã liên hệ'")
    mark_as_contacted.short_description = "Đánh dấu đã liên hệ"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
        self.message_user(request, f"Đã cập nhật {queryset.count()} đơn thành 'Hoàn thành'")
    mark_as_completed.short_description = "Đánh dấu hoàn thành"


@admin.register(AdmissionDocument)
class AdmissionDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'admission', 'document_type', 'school_year', 'file_size', 'download_count', 'is_active', 'order']
    list_filter = ['admission', 'document_type', 'school_year', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['title', 'description']
    readonly_fields = ['download_count', 'file_size', 'created_at', 'updated_at']

    fieldsets = (
        ('Thông tin tài liệu', {
            'fields': ('admission', 'title', 'description', 'document_type', 'school_year')
        }),
        ('File', {
            'fields': ('file', 'file_size')
        }),
        ('Cài đặt', {
            'fields': ('is_active', 'order', 'download_count')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
