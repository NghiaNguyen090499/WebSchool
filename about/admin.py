from django.contrib import admin

from .models import AboutPage, AboutPdfDocument, AboutPdfPageImage, AboutSection


class AboutSectionInline(admin.StackedInline):
    """Inline admin for managing AboutSection within AboutPage"""

    model = AboutSection
    extra = 0
    ordering = ["order"]
    fieldsets = (
        (
            "Section Settings",
            {
                "fields": (("order", "layout", "background"),),
            },
        ),
        (
            "Content",
            {
                "fields": ("eyebrow", "title", "subtitle", "content", "timeline", "kpi", "highlight_text"),
            },
        ),
        (
            "Visual (Upload image here)",
            {
                "fields": (
                    "image",
                    ("feature_image_1", "feature_image_2", "feature_image_3"),
                    ("feature_image_4", "feature_image_5", "feature_image_6"),
                    ("stat_number", "stat_label"),
                ),
                "description": "Use image for split layout and feature_image_1..6 for feature cards.",
            },
        ),
        (
            "Call to Action",
            {
                "fields": (("cta_text", "cta_url"), ("cta_secondary_text", "cta_secondary_url")),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ["page_type", "title", "section_count", "updated_at"]
    list_filter = ["page_type"]
    search_fields = ["title", "content"]
    inlines = [AboutSectionInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("page_type", "title", "image"),
            },
        ),
        (
            "Legacy Content",
            {
                "fields": ("content",),
                "classes": ("collapse",),
                "description": "This field is for backwards compatibility. Use Sections below for new content.",
            },
        ),
    )

    def section_count(self, obj):
        return obj.sections.count()

    section_count.short_description = "Sections"


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ["page", "order", "layout", "background", "title"]
    list_filter = ["layout", "background", "page"]
    ordering = ["page", "order"]
    fieldsets = (
        (
            "Section Settings",
            {
                "fields": (("page", "order"), ("layout", "background")),
            },
        ),
        (
            "Content",
            {
                "fields": ("eyebrow", "title", "subtitle", "content", "timeline", "kpi", "highlight_text"),
            },
        ),
        (
            "Visual",
            {
                "fields": (
                    "image",
                    ("feature_image_1", "feature_image_2", "feature_image_3"),
                    ("feature_image_4", "feature_image_5", "feature_image_6"),
                    ("stat_number", "stat_label"),
                ),
            },
        ),
        (
            "Call to Action",
            {
                "fields": (("cta_text", "cta_url"), ("cta_secondary_text", "cta_secondary_url")),
                "classes": ("collapse",),
            },
        ),
    )


class AboutPdfPageImageInline(admin.TabularInline):
    model = AboutPdfPageImage
    extra = 0
    ordering = ["order"]


@admin.register(AboutPdfDocument)
class AboutPdfDocumentAdmin(admin.ModelAdmin):
    list_display = ["page_type", "title", "subtitle"]
    search_fields = ["page_type", "title", "subtitle"]
    inlines = [AboutPdfPageImageInline]
