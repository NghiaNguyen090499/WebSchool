from django.contrib import admin

from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "degree", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("name", "degree", "languages")
    prepopulated_fields = {"slug": ("name",)}
