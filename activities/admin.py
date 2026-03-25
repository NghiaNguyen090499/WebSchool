from django.contrib import admin

from .models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "start_date", "end_date", "is_active")
    list_filter = ("type", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
