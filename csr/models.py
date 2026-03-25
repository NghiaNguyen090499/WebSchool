from django.db import models
from django.utils.text import slugify


class CSRProject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    impact_metrics = models.TextField(
        blank=True,
        help_text="Mỗi dòng là một chỉ số tác động, ví dụ: '2.000+ học sinh thụ hưởng'.",
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Dự án CSR"
        verbose_name_plural = "Dự án CSR"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while CSRProject.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_impact_metrics_list(self):
        return [item.strip() for item in self.impact_metrics.splitlines() if item.strip()]


class CSRImage(models.Model):
    project = models.ForeignKey(
        CSRProject,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="csr/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Ảnh CSR"
        verbose_name_plural = "Ảnh CSR"

    def __str__(self):
        return f"{self.project.title} - {self.caption or self.image.name}"


# ═══════════════════════════════════════════════════
#  JOURNEY PROGRAM – Hành trình thiện nguyện
# ═══════════════════════════════════════════════════

class JourneyProgram(models.Model):
    """Một chương trình trong hành trình thiện nguyện 15+ năm của MIS."""

    title = models.CharField("Tên chương trình", max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    period = models.CharField(
        "Giai đoạn",
        max_length=50,
        help_text="Ví dụ: '2008 – 2017', 'Hàng năm', 'Mỗi dịp Tết'",
    )
    icon = models.CharField(
        "Icon FontAwesome",
        max_length=50,
        default="fa-hand-holding-heart",
        help_text="Class icon FontAwesome, ví dụ: fa-moon, fa-gift",
    )
    short_description = models.TextField(
        "Mô tả ngắn",
        help_text="Hiển thị trên card. 1-2 câu.",
    )
    full_description = models.TextField(
        "Mô tả đầy đủ",
        help_text="Hiển thị trong modal chi tiết. Dùng <br> để xuống dòng.",
    )
    cover_image = models.ImageField(
        "Ảnh bìa",
        upload_to="csr/journey/covers/",
        blank=True,
        null=True,
        help_text="Ảnh chính hiển thị trên card và header modal.",
    )
    tags = models.TextField(
        "Tags",
        blank=True,
        help_text="Mỗi dòng là một tag, ví dụ: '10 năm đồng hành'",
    )
    order = models.PositiveIntegerField("Thứ tự", default=0)
    is_active = models.BooleanField("Hiển thị", default=True)
    is_featured = models.BooleanField(
        "Nổi bật",
        default=False,
        help_text="3 chương trình nổi bật hiện trước, còn lại ẩn sau 'Xem thêm'.",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Chương trình Journey"
        verbose_name_plural = "Chương trình Journey"

    def __str__(self):
        return f"{self.title} ({self.period})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title) or "journey"
        slug = base_slug
        counter = 1
        while JourneyProgram.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_tags_list(self):
        """Trả về danh sách tags từ trường text."""
        return [t.strip() for t in self.tags.splitlines() if t.strip()]

    @property
    def primary_image_url(self):
        """URL ảnh cover, hoặc None nếu không có."""
        if self.cover_image:
            return self.cover_image.url
        return None


class JourneyImage(models.Model):
    """Ảnh gallery cho một chương trình Journey."""

    program = models.ForeignKey(
        JourneyProgram,
        on_delete=models.CASCADE,
        related_name="gallery_images",
    )
    image = models.ImageField("Ảnh", upload_to="csr/journey/gallery/")
    caption = models.CharField("Chú thích", max_length=200, blank=True)
    order = models.PositiveIntegerField("Thứ tự", default=0)
    is_active = models.BooleanField("Hiển thị", default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Ảnh Journey"
        verbose_name_plural = "Ảnh Journey"

    def __str__(self):
        return f"{self.program.title} - {self.caption or self.image.name}"
