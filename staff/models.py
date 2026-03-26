from django.db import models
from django.utils.text import slugify


class Staff(models.Model):
    ROLE_CHOICES = [
        ("teacher", "Giáo viên"),
        ("admin", "Quản trị"),
        ("ai", "AI / Công nghệ"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="teacher")
    degree = models.CharField(max_length=100, blank=True)
    languages = models.CharField(
        max_length=200,
        blank=True,
        help_text="Danh sách ngôn ngữ, phân tách bằng dấu phẩy.",
    )
    specialties = models.TextField(blank=True)
    avatar = models.ImageField(max_length=255, upload_to="staff/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["role", "name"]
        verbose_name = "Nhân sự"
        verbose_name_plural = "Đội ngũ nhân sự"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Staff.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_languages_list(self):
        return [item.strip() for item in self.languages.split(",") if item.strip()]
