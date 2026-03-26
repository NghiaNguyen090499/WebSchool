from django.db import models
from django.utils.text import slugify


class Activity(models.Model):
    TYPE_CHOICES = [
        ("extracurricular", "Ngoại khóa"),
        ("summer_camp", "Trại hè"),
        ("international", "Quốc tế"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="extracurricular")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_date", "title"]
        verbose_name = "Hoạt động"
        verbose_name_plural = "Hoạt động ngoại khóa"

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
        while Activity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def get_date_range_display(self):
        if self.end_date and self.end_date != self.start_date:
            return f"{self.start_date:%d/%m/%Y} - {self.end_date:%d/%m/%Y}"
        return f"{self.start_date:%d/%m/%Y}"
