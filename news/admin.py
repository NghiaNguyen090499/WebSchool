from django.contrib import admin
from .models import Category, News


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_archived', 'created_at']
    list_filter = ['is_archived', 'category', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    actions = ['archive_selected', 'unarchive_selected']

    def get_queryset(self, request):
        """Show all news (including archived) in admin."""
        return News.all_objects.all()

    def archive_selected(self, request, queryset):
        queryset.update(is_archived=True)
    archive_selected.short_description = "Archive selected news"

    def unarchive_selected(self, request, queryset):
        queryset.update(is_archived=False)
    unarchive_selected.short_description = "Unarchive selected news"








