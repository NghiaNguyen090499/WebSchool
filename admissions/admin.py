from django.contrib import admin
from .models import AdmissionInfo, AdmissionHighlight, AdmissionRegistration


class AdmissionHighlightInline(admin.TabularInline):
    model = AdmissionHighlight
    extra = 1
    fields = ['title', 'description', 'icon', 'order']


@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['level', 'title', 'school_year', 'is_active', 'is_featured', 'order', 'updated_at']
    list_filter = ['is_active', 'is_featured', 'school_year']
    list_editable = ['is_active', 'is_featured', 'order']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [AdmissionHighlightInline]
    
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
    list_display = ['student_name', 'admission', 'parent_name', 'parent_phone', 'status', 'created_at']
    list_filter = ['status', 'admission', 'created_at', 'student_gender']
    list_editable = ['status']
    search_fields = ['student_name', 'parent_name', 'parent_phone', 'parent_email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Cấp học đăng ký', {
            'fields': ('admission', 'status')
        }),
        ('Thông tin phụ huynh', {
            'fields': ('parent_name', 'parent_phone', 'parent_email')
        }),
        ('Thông tin học sinh', {
            'fields': ('student_name', 'student_dob', 'student_gender', 'current_school', 'current_grade')
        }),
        ('Địa chỉ liên hệ', {
            'fields': ('address', 'district', 'city')
        }),
        ('Thông tin bổ sung', {
            'fields': ('how_did_you_know', 'note')
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
