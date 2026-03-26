import json
from io import BytesIO
from pathlib import PurePosixPath

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, UnidentifiedImageError


class AboutPage(models.Model):
    PAGE_CHOICES = [
        # Về chúng tôi section
        ('mission', 'Về chúng tôi'),
        ('vision', 'Giá trị cốt lõi'),
        ('principal', 'Thông điệp Tổng Giám đốc'),
        ('strengths', '8 điểm mạnh khác biệt'),
        ('strategy', 'Chiến lược phát triển'),
        ('structure', 'Cơ cấu tổ chức MIS'),
        ('culture', 'Quy định văn hóa MIS'),
        ('boarding', 'Môi trường nội trú'),
        ('happiness', 'Trường Văn minh – Hạnh phúc'),
        ('liberal', 'Giáo dục khai phóng'),
        # Chương trình học - Academics
        ('academics', 'Tổng quan Chương trình Giáo dục'),
        ('preschool', 'Chương trình Mầm non (3-6 tuổi)'),
        ('primary', 'Chương trình Tiểu học (Lớp 1-5)'),
        ('middle', 'Chương trình THCS (Lớp 6-9)'),
        ('high', 'Chương trình THPT (Lớp 10-12)'),
        # Tổng quan chương trình môn học
        ('overview_math', 'Tổng quan Chương trình môn Toán'),
        ('overview_literature', 'Tổng quan Chương trình môn Ngữ văn'),
        ('overview_english', 'Tổng quan Chương trình Tiếng Anh'),
        ('overview_chinese', 'Tổng quan Chương trình Tiếng Trung'),
        # Chương trình chuyên sâu
        ('tnst', 'Chương trình Trải nghiệm sáng tạo (TNST)'),
        ('steam', 'Chương trình STEAM với Công nghệ sáng tạo'),
        ('robotics', 'Chương trình Robotic'),
        ('lifeskills', 'Chương trình Kỹ năng sống'),
        ('creative_movement', 'Chương trình Tâm vấn động'),
        # Khung kế hoạch
        ('schedule_2025', 'Khung Kế hoạch năm học 2026-2027'),
        ('schedule_hd', 'Khung Kế hoạch HĐ phòng trào năm học 2026-2027'),
        # Tuyển sinh
        ('whymis', 'Tại sao chọn MIS?'),
    ]
    PAGE_CHOICES += [
        ('strategy_2025_2028', 'Strategy 2025-2028'),
        ('vision_2033', 'Vision 2033'),
        ('future_ai', 'Future With AI'),
        ('edtech', 'Hệ sinh thái EdTech 4.0'),
        ('partners', 'Đối Tác Chiến Lược'),
    ]
    
    page_type = models.CharField(max_length=30, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True, help_text="Legacy content field - use sections for new pages")
    image = models.ImageField(max_length=255, upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'
    
    def __str__(self):
        return self.get_page_type_display()


class AboutSection(models.Model):
    """Structured content sections for Nord Anglia style pages"""
    
    LAYOUT_CHOICES = [
        ('hero', 'Hero Section'),
        ('text_left', 'Text Left, Image Right'),
        ('text_right', 'Text Right, Image Left'),
        ('full_text', 'Full Width Text'),
        ('stats', 'Statistics/Numbers'),
        ('quote', 'Quote/Testimonial'),
        ('cta', 'Call to Action'),
        ('features', 'Feature Grid'),
        ('future_ai', 'Future With AI'),
    ]
    
    BACKGROUND_CHOICES = [
        ('white', 'White'),
        ('light', 'Light Grey'),
        ('navy', 'Navy Blue'),
        ('accent', 'Teal Accent'),
        ('gradient', 'Gradient'),
    ]
    
    page = models.ForeignKey(AboutPage, related_name='sections', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, help_text="Order of section on page")
    layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='full_text')
    background = models.CharField(max_length=20, choices=BACKGROUND_CHOICES, default='white')
    
    # Content fields
    eyebrow = models.CharField(max_length=100, blank=True, help_text="Small text above title (e.g., 'WHY MIS')")
    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)

    # Timeline/KPI fields
    timeline = models.TextField(
        blank=True,
        help_text="Timeline items (one per line or JSON list)",
    )
    kpi = models.TextField(
        blank=True,
        help_text="KPI items (one per line or JSON list)",
    )
    
    # Visual fields
    image = models.ImageField(max_length=255, upload_to='about/sections/', blank=True, null=True)
    feature_image_1 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    feature_image_2 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    feature_image_3 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    feature_image_4 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    feature_image_5 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    feature_image_6 = models.ImageField(max_length=255, upload_to='about/feature_cards/', blank=True, null=True)
    highlight_text = models.CharField(max_length=100, blank=True, help_text="Text to highlight in accent color")
    stat_number = models.CharField(max_length=50, blank=True, help_text="Large number for stats (e.g., '84%')")
    stat_label = models.CharField(max_length=100, blank=True, help_text="Label below stat number")
    
    # CTA fields
    cta_text = models.CharField(max_length=100, blank=True, help_text="Button text")
    cta_url = models.CharField(max_length=200, blank=True, help_text="Button URL")
    cta_secondary_text = models.CharField(max_length=100, blank=True)
    cta_secondary_url = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'About Section'
        verbose_name_plural = 'About Sections'
        ordering = ['page', 'order']
    
    def _parse_list_field(self, value):
        if not value:
            return []
        try:
            parsed = json.loads(value)
        except (TypeError, ValueError):
            parsed = None
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
        lines = [line.strip() for line in value.splitlines()]
        return [line for line in lines if line]

    def get_timeline_list(self):
        return self._parse_list_field(self.timeline)

    def get_kpi_list(self):
        return self._parse_list_field(self.kpi)

    def __str__(self):
        return f"{self.page} - {self.get_layout_display()} ({self.order})"

class AboutPdfDocument(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    page_type = models.SlugField(
        max_length=255,
        unique=True,
        help_text="Slug or page_type used to map the PDF to a page",
    )
    pdf_file = models.FileField(max_length=255, upload_to='about/pdfs/')
    hero_image = models.ImageField(max_length=255, upload_to='about/pdfs/hero/', blank=True, null=True)

    class Meta:
        verbose_name = 'About PDF Document'
        verbose_name_plural = 'About PDF Documents'

    def __str__(self):
        return self.title


class AboutPdfPageImage(models.Model):
    WEBP_QUALITY = 78
    AVIF_QUALITY = 55

    document = models.ForeignKey(
        AboutPdfDocument,
        on_delete=models.CASCADE,
        related_name='pages',
    )
    image = models.ImageField(max_length=255, upload_to='about/pdfs/pages/')
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    image_webp = models.ImageField(max_length=255, upload_to='about/pdfs/pages/', null=True, blank=True, editable=False)
    image_avif = models.ImageField(max_length=255, upload_to='about/pdfs/pages/', null=True, blank=True, editable=False)
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'About PDF Page Image'
        verbose_name_plural = 'About PDF Page Images'

    def __str__(self):
        return f'{self.document.page_type} - {self.order}'

    def save(self, *args, **kwargs):
        source_changed = self._source_image_changed()
        super().save(*args, **kwargs)
        if self.image:
            self.refresh_optimized_assets(force=source_changed, save=True)

    def refresh_optimized_assets(self, force=False, save=True):
        """Create AVIF/WebP derivatives and persist missing dimensions."""
        if not self.image:
            return False

        needs_dimensions = not self.image_width or not self.image_height
        needs_webp = force or not self.image_webp
        needs_avif = force or not self.image_avif
        if not (needs_dimensions or needs_webp or needs_avif):
            return False

        updated_fields = []
        try:
            self.image.open("rb")
            with Image.open(self.image) as source_image:
                source_image.load()
                width, height = source_image.size
                has_alpha = source_image.mode in {"RGBA", "LA"} or (
                    source_image.mode == "P" and "transparency" in source_image.info
                )
                prepared = source_image.convert("RGBA" if has_alpha else "RGB")
        except (FileNotFoundError, UnidentifiedImageError, OSError, ValueError):
            return False
        finally:
            try:
                self.image.close()
            except Exception:
                pass

        if needs_dimensions and (
            self.image_width != width or self.image_height != height
        ):
            self.image_width = width
            self.image_height = height
            updated_fields.extend(["image_width", "image_height"])

        if needs_webp:
            webp_name = self._variant_name("webp")
            self._replace_optimized_file("image_webp", webp_name)
            webp_payload = self._encode_variant(
                prepared,
                fmt="WEBP",
                quality=self.WEBP_QUALITY,
                method=6,
            )
            if webp_payload:
                self.image_webp.save(webp_name, webp_payload, save=False)
                updated_fields.append("image_webp")

        if needs_avif:
            avif_name = self._variant_name("avif")
            self._replace_optimized_file("image_avif", avif_name)
            avif_payload = self._encode_variant(
                prepared,
                fmt="AVIF",
                quality=self.AVIF_QUALITY,
            )
            if avif_payload:
                self.image_avif.save(avif_name, avif_payload, save=False)
                updated_fields.append("image_avif")

        if save and updated_fields:
            super().save(update_fields=updated_fields)
        return bool(updated_fields)

    def _source_image_changed(self):
        if not self.image:
            return False
        if not self.pk:
            return True
        previous = (
            type(self)
            .objects.filter(pk=self.pk)
            .only("image")
            .first()
        )
        if not previous:
            return True
        return previous.image.name != self.image.name

    def _variant_name(self, extension):
        source_path = PurePosixPath(self.image.name)
        return str(source_path.with_suffix(f".{extension}"))

    def _replace_optimized_file(self, field_name, target_name):
        optimized_field = getattr(self, field_name)
        storage = optimized_field.storage
        if optimized_field.name and optimized_field.name != target_name:
            storage.delete(optimized_field.name)
        if storage.exists(target_name):
            storage.delete(target_name)

    @staticmethod
    def _encode_variant(image_obj, fmt, quality, **extra_kwargs):
        output = BytesIO()
        try:
            image_obj.save(output, format=fmt, quality=quality, **extra_kwargs)
        except (KeyError, OSError, ValueError):
            return None
        return ContentFile(output.getvalue())
