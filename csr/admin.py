from django.contrib import admin
from django.utils.html import format_html

from .models import CSRImage, CSRProject, JourneyImage, JourneyProgram


# ═══ CSR PROJECT ═══

class CSRImageInline(admin.TabularInline):
    model = CSRImage
    extra = 0
    ordering = ["order"]


@admin.register(CSRProject)
class CSRProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CSRImageInline]


@admin.register(CSRImage)
class CSRImageAdmin(admin.ModelAdmin):
    list_display = ("project", "caption", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


# ═══ JOURNEY PROGRAM ═══

class JourneyImageInline(admin.TabularInline):
    model = JourneyImage
    extra = 1
    ordering = ["order"]
    fields = ("image", "caption", "order", "is_active", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px; border-radius:6px;" />',
                obj.image.url,
            )
        return "—"
    image_preview.short_description = "Xem trước"


@admin.register(JourneyProgram)
class JourneyProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "period", "order", "is_featured", "is_active", "cover_preview")
    list_editable = ("order", "is_featured", "is_active")
    list_filter = ("is_active", "is_featured")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [JourneyImageInline]
    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("title", "slug", "period", "icon", "order"),
        }),
        ("Nội dung", {
            "fields": ("short_description", "full_description", "tags"),
        }),
        ("Hình ảnh", {
            "fields": ("cover_image",),
        }),
        ("Hiển thị", {
            "fields": ("is_active", "is_featured"),
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height:40px; border-radius:6px;" />',
                obj.cover_image.url,
            )
        return "—"
    cover_preview.short_description = "Ảnh bìa"


@admin.register(JourneyImage)
class JourneyImageAdmin(admin.ModelAdmin):
    list_display = ("program", "caption", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "program")
