from django.contrib import admin
from .models import AboutPage


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['page_type', 'title', 'updated_at']
    list_filter = ['page_type']



