from django.contrib import admin
from django.utils.html import format_html
from .models import (
    CoreValue, CoreValuesPage, Statistic, MenuItem, TrainingProgramGroup, TrainingProgram, SchoolInfo, Campus,
    WebsiteGoal, StudentLifePage, HeroSlide, Achievement, ParentTestimonial,
    Partner, FounderMessage, StudentSpotlight, Pillar, Facility, Podcast, ProgramContentSource,
    MISPrototypeSiteContent, MISPrototypePage,
    ProgramOverviewPage, ProgramOverviewImage, MediaAsset,
    TimetableUpload
)


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']
    search_fields = ['title']


@admin.register(CoreValuesPage)
class CoreValuesPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_editable = ['is_active']
    search_fields = ['title', 'subtitle', 'social_title']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order']
    list_editable = ['order', 'value']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'position', 'order', 'parent', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['position', 'is_active', 'parent']
    search_fields = ['title', 'link']


@admin.register(TrainingProgramGroup)
class TrainingProgramGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'partner_name', 'group', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'color', 'group']
    search_fields = ['name', 'short_name', 'partner_name']
    prepopulated_fields = {'slug': ('short_name',)}
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('slug', 'group', 'name', 'short_name', 'tagline', 'description')
        }),
        ('Đối tác đào tạo', {
            'fields': ('partner_name', 'partner_description', 'partner_logo')
        }),
        ('Nội dung chương trình', {
            'fields': ('highlights', 'curriculum', 'achievements', 'commitments')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('grade_levels', 'icon', 'color', 'image', 'order', 'is_active')
        }),
    )


@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    list_display = ['name_vn', 'short_name', 'hotline', 'is_active', 'updated_at']
    list_editable = ['is_active']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name_vn', 'name_en', 'short_name', 'short_description')
        }),
        ('Liên hệ', {
            'fields': ('address', 'hotline', 'admissions_email', 'general_email', 'current_website')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'youtube_url', 'tiktok_url', 'zalo_url', 'instagram_url', 'linkedin_url')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon')
        }),
        ('Cài đặt', {
            'fields': ('is_active', 'updated_at')
        }),
    )
    readonly_fields = ['updated_at']
    
    def has_add_permission(self, request):
        # Chỉ cho phép tạo 1 bản ghi
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'is_primary', 'is_active', 'order']
    list_editable = ['is_primary', 'is_active', 'order']
    list_filter = ['is_active', 'is_primary']
    search_fields = ['name', 'address', 'phone', 'email']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('school', 'name', 'address')
        }),
        ('Liên hệ', {
            'fields': ('phone', 'email', 'map_embed_url')
        }),
        ('Cài đặt', {
            'fields': ('is_primary', 'is_active', 'order', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WebsiteGoal)
class WebsiteGoalAdmin(admin.ModelAdmin):
    list_display = ['goal_type', 'priority', 'is_active']
    list_editable = ['priority', 'is_active']
    list_filter = ['is_active', 'goal_type']
    search_fields = ['description']


@admin.register(StudentLifePage)
class StudentLifePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'order', 'updated_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'description', 'content')
        }),
        ('Nội dung', {
            'fields': ('activities', 'clubs', 'events', 'facilities')
        }),
        ('Hình ảnh', {
            'fields': ('banner_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Cài đặt', {
            'fields': ('is_active', 'order', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


class ProgramOverviewImageInline(admin.TabularInline):
    model = ProgramOverviewImage
    extra = 0


@admin.register(ProgramOverviewPage)
class ProgramOverviewPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'order', 'is_active', 'updated_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'subtitle', 'description', 'source_url']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProgramOverviewImageInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'subtitle', 'description')
        }),
        ('Nguồn & hiển thị', {
            'fields': ('source_url', 'hero_image_url', 'hero_image')
        }),
        ('Cài đặt', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )


# ============================================
# NEW MODELS - Dynamic Homepage Content
# ============================================

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'slide_type', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'slide_type']
    search_fields = ['title', 'subtitle', 'description']
    ordering = ['order']
    
    fieldsets = (
        ('Nội dung chính', {
            'fields': ('title', 'title_highlight', 'subtitle', 'slogan', 'description')
        }),
        ('Badge/Tag', {
            'fields': ('badge_text', 'badge_icon', 'slide_type')
        }),
        ('Nút bấm (CTA)', {
            'fields': ('cta_primary_text', 'cta_primary_url', 'cta_primary_icon', 
                       'cta_secondary_text', 'cta_secondary_url')
        }),
        ('Hình ảnh', {
            'fields': ('image',)
        }),
        ('Cài đặt hiển thị', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius: 8px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Ảnh"


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'stat_value', 'category', 'color', 'is_stat', 'is_card', 'order', 'is_active', 'image_preview']
    list_editable = ['order', 'is_active', 'is_stat', 'is_card']
    list_filter = ['is_active', 'category', 'color', 'is_stat', 'is_card']
    search_fields = ['title', 'description', 'stat_value', 'stat_label']
    ordering = ['order']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Số liệu thống kê', {
            'fields': ('stat_value', 'stat_label'),
            'description': "Hiển thị trong phần số liệu (VD: 98% - Tỷ lệ đậu Đại học)"
        }),
        ('Chi tiết thành tích', {
            'fields': ('title', 'description', 'icon', 'image', 'image_preview', 'tags')
        }),
        ('Phân loại', {
            'fields': ('category', 'color')
        }),
        ('Kiểu hiển thị', {
            'fields': ('is_stat', 'is_card'),
            'description': "Chọn hiển thị dạng số liệu (stats) và/hoặc dạng card"
        }),
        ('Cài đặt', {
            'fields': ('order', 'is_active')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="border-radius: 10px; object-fit: cover;" />',
                obj.image.url,
            )
        return "-"
    image_preview.short_description = "Image"


@admin.register(ParentTestimonial)
class ParentTestimonialAdmin(admin.ModelAdmin):
    list_display = ['parent_name', 'student_class', 'title', 'has_video', 'order', 'is_active', 'photo_preview']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'has_video']
    search_fields = ['parent_name', 'student_class', 'title', 'short_quote']
    ordering = ['order']
    
    fieldsets = (
        ('Thông tin phụ huynh', {
            'fields': ('parent_name', 'student_class', 'photo')
        }),
        ('Nội dung chia sẻ', {
            'fields': ('title', 'short_quote', 'full_content', 'achievement')
        }),
        ('Video', {
            'fields': ('has_video', 'video_url'),
            'description': "Paste URL video từ Google Drive hoặc YouTube"
        }),
        ('Cài đặt', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="70" style="border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Ảnh"


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'logo_preview', 'show_in_marquee', 'order', 'is_active']
    list_editable = ['order', 'is_active', 'show_in_marquee']
    list_filter = ['is_active', 'partner_type', 'show_in_marquee']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Thông tin đối tác', {
            'fields': ('name', 'logo', 'url', 'description')
        }),
        ('Phân loại', {
            'fields': ('partner_type',)
        }),
        ('Hiển thị', {
            'fields': ('show_in_marquee', 'order', 'is_active')
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="80" style="max-height: 40px; object-fit: contain;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = "Logo"


@admin.register(FounderMessage)
class FounderMessageAdmin(admin.ModelAdmin):
    list_display = ['founder_name', 'founder_title', 'is_active', 'updated_at', 'photo_preview']
    list_editable = ['is_active']
    readonly_fields = ['updated_at']
    
    fieldsets = (
        ('Thông tin người sáng lập', {
            'fields': ('founder_name', 'founder_title', 'founder_photo')
        }),
        ('Trích dẫn chính', {
            'fields': ('main_quote',),
            'description': "Câu quote ngắn hiển thị trên trang chủ"
        }),
        ('Thông điệp đầy đủ', {
            'fields': ('greeting', 'full_message', 'closing_message'),
            'description': "Nội dung hiển thị trong modal khi click 'Xem đầy đủ'"
        }),
        ('Cài đặt', {
            'fields': ('is_active', 'updated_at')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.founder_photo:
            return format_html('<img src="{}" width="60" height="60" style="border-radius: 50%; object-fit: cover;" />', obj.founder_photo.url)
        return "-"
    photo_preview.short_description = "Ảnh"
    
    def has_add_permission(self, request):
        # Chỉ cho phép tạo 1 thông điệp
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(StudentSpotlight)
class StudentSpotlightAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'title', 'category', 'is_featured', 'order', 'is_active', 'photo_preview']
    list_editable = ['order', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'category']
    search_fields = ['student_name', 'title', 'achievement', 'student_class']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        ('Thông tin học sinh', {
            'fields': ('student_name', 'student_class', 'photo')
        }),
        ('Thành tích', {
            'fields': ('title', 'achievement', 'category', 'tags')
        }),
        ('Trích dẫn', {
            'fields': ('quote',),
            'classes': ('collapse',)
        }),
        ('Liên kết', {
            'fields': ('article_url',),
            'classes': ('collapse',)
        }),
        ('Cài đặt hiển thị', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60" height="45" style="border-radius: 6px; object-fit: cover;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = "Ảnh"


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ["title", "order", "is_active"]
    list_editable = ["order", "is_active"]
    search_fields = ["title", "short_description"]


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "order", "is_active"]
    list_editable = ["order", "is_active"]
    list_filter = ["category", "is_active"]
    search_fields = ["name", "description"]


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['title', 'episode_number', 'host_name', 'is_featured', 'order', 'is_active', 'thumbnail_preview']
    list_editable = ['order', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['title', 'description', 'host_name', 'guest_name']
    ordering = ['-episode_number', 'order']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'description', 'youtube_url', 'thumbnail')
        }),
        ('Người tham gia', {
            'fields': ('host_name', 'guest_name')
        }),
        ('Thông tin tập', {
            'fields': ('episode_number', 'duration', 'published_date')
        }),
        ('Cài đặt hiển thị', {
            'fields': ('is_featured', 'order', 'is_active')
        }),
    )
    
    def thumbnail_preview(self, obj):
        thumbnail_url = obj.get_thumbnail_url()
        if thumbnail_url:
            return format_html('<img src="{}" width="120" style="border-radius: 6px;" />', thumbnail_url)
        return "-"
    thumbnail_preview.short_description = "Thumbnail"


@admin.register(MISPrototypeSiteContent)
class MISPrototypeSiteContentAdmin(admin.ModelAdmin):
    list_display = ["year", "title", "version", "is_active", "updated_at"]
    list_editable = ["is_active"]
    search_fields = ["year", "title", "source_doc", "version"]
    readonly_fields = ["updated_at"]
    fieldsets = (
        ("Core", {"fields": ("year", "title", "badge", "lead", "meta_description")}),
        (
            "CTAs",
            {
                "fields": (
                    "cta_primary_label",
                    "cta_primary_href",
                    "cta_primary_icon",
                    "cta_secondary_label",
                    "cta_secondary_href",
                    "cta_secondary_icon",
                )
            },
        ),
        ("Metrics", {"fields": ("metrics",)}),
        ("Metadata", {"fields": ("source_doc", "approved_at", "version", "is_active", "updated_at")}),
    )


@admin.register(MISPrototypePage)
class MISPrototypePageAdmin(admin.ModelAdmin):
    list_display = ["year", "page_key", "nav_label", "order", "version", "is_active", "updated_at"]
    list_editable = ["order", "is_active"]
    list_filter = ["year", "is_active"]
    search_fields = ["year", "page_key", "nav_label", "title", "source_doc", "version"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Core", {"fields": ("year", "page_key", "nav_label", "title", "browser_title", "meta_description")}),
        ("Content", {"fields": ("body_html", "blocks")}),
        ("Metadata", {"fields": ("source_doc", "approved_at", "version", "order", "is_active")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(ProgramContentSource)
class ProgramContentSourceAdmin(admin.ModelAdmin):
    list_display = ["year", "version", "source_doc", "is_active", "updated_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "year"]
    search_fields = ["year", "version", "source_doc"]
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        ("Core", {"fields": ("year", "content")}),
        ("Metadata", {"fields": ("source_doc", "approved_at", "version", "is_active")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "slug",
        "file_type",
        "category",
        "page_target",
        "block_target",
        "is_approved",
        "usage_rights_status",
        "preview",
        "updated_at",
    ]
    list_filter = [
        "is_approved",
        "file_type",
        "category",
        "usage_rights_status",
        "page_target",
        "block_target",
    ]
    search_fields = [
        "slug",
        "original_name",
        "caption",
        "alt_text",
        "notes",
        "page_target",
        "block_target",
    ]
    readonly_fields = ["checksum", "file_size", "created_at", "updated_at", "preview"]

    fieldsets = (
        ("Files", {"fields": ("file", "file_webp", "file_jpeg", "poster", "preview")}),
        ("Targeting", {"fields": ("file_type", "category", "page_target", "block_target", "tags")}),
        ("Content", {"fields": ("caption", "alt_text", "notes")}),
        ("Attributes", {"fields": ("width", "height", "duration", "source", "slug", "original_name")}),
        (
            "Compliance",
            {
                "fields": (
                    "is_approved",
                    "needs_consent",
                    "contains_student",
                    "contains_parent",
                    "usage_rights_status",
                )
            },
        ),
        ("System", {"fields": ("checksum", "file_size", "created_at", "updated_at")}),
    )

    def preview(self, obj):
        if obj.file_type == "image":
            image_file = obj.file_jpeg or obj.file_webp or obj.file
            if image_file:
                return format_html(
                    '<img src="{}" width="120" style="border-radius: 8px; object-fit: cover;" />',
                    image_file.url,
                )
        if obj.file:
            return format_html('<a href="{}" target="_blank" rel="noopener">Open file</a>', obj.file.url)
        return "-"

    preview.short_description = "Preview"

@admin.register(TimetableUpload)
class TimetableUploadAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title']
    readonly_fields = ['uploaded_at']
