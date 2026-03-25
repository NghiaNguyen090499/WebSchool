from django.contrib import admin
from .models import ContactMessage, ConsultationRequest, ChatbotLead


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 'email', 'subject', 'grade_level',
        'interest_visit', 'interest_curriculum', 'interest_admission_process',
        'is_read', 'created_at',
    ]
    list_filter = [
        'is_read', 'subject', 'grade_level',
        'interest_visit', 'interest_curriculum', 'interest_admission_process',
        'created_at',
    ]
    list_editable = ['is_read']
    search_fields = ['name', 'phone', 'email', 'subject']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Thông tin liên hệ', {
            'fields': ('name', 'phone', 'email', 'subject', 'grade_level')
        }),
        ('Chương trình quan tâm', {
            'fields': ('interest_visit', 'interest_curriculum', 'interest_admission_process')
        }),
        ('Nội dung & trạng thái', {
            'fields': ('message', 'is_read')
        }),
        ('Thời gian', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'phone', 'grade_level',
        'interest_visit', 'interest_curriculum', 'interest_admission_process',
        'is_contacted', 'created_at',
    ]
    list_filter = [
        'is_contacted', 'grade_level',
        'interest_visit', 'interest_curriculum', 'interest_admission_process',
        'created_at',
    ]
    list_editable = ['is_contacted']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Thông tin phụ huynh', {
            'fields': ('name', 'phone', 'email', 'grade_level')
        }),
        ('Chương trình quan tâm', {
            'fields': ('interest_visit', 'interest_curriculum', 'interest_admission_process')
        }),
        ('Nội dung & trạng thái', {
            'fields': ('message', 'is_contacted', 'notes')
        }),
        ('Thời gian', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatbotLead)
class ChatbotLeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'is_contacted', 'created_at']
    list_filter = ['is_contacted', 'created_at']
    list_editable = ['is_contacted']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
