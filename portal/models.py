from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from core.validators import validate_upload_extension, validate_upload_file_size


class PortalPage(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    TYPE_CHOICES = [
        ("general", "General"),
        ("about", "About"),
        ("admissions", "Admissions"),
        ("news", "News"),
        ("policy", "Policy"),
        ("portal", "Portal"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    page_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default="general")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    content = models.TextField(blank=True)
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    og_image = models.ImageField(upload_to="portal/og/", blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portal_pages_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portal_pages_updated",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == "published" and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class PortalPageRevision(models.Model):
    page = models.ForeignKey(PortalPage, on_delete=models.CASCADE, related_name="revisions")
    snapshot = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portal_page_revisions",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.page} @ {self.created_at:%Y-%m-%d %H:%M}"


class PortalMediaAsset(models.Model):
    FILE_TYPE_CHOICES = [
        ("image", "Image"),
        ("document", "Document"),
        ("other", "Other"),
    ]

    file = models.FileField(
        upload_to="portal/media/",
        validators=[validate_upload_extension, validate_upload_file_size],
    )
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default="image")
    alt_text = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portal_media_assets",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.file.name


class PortalAuditLog(models.Model):
    ACTION_CHOICES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("publish", "Publish"),
        ("unpublish", "Unpublish"),
        ("preview", "Preview"),
        ("upload", "Upload"),
    ]

    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    page = models.ForeignKey(
        PortalPage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="portal_audit_logs",
    )
    details = models.TextField(blank=True)
    target_model = models.CharField(max_length=50, blank=True)
    target_object_id = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        target = self.page or self.target_model or "portal"
        return f"{self.action} - {target}"
