from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ActiveNewsManager(models.Manager):
    """Only return non-archived news by default."""
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)


class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='news/thumbnails/', blank=True, null=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short summary for listing pages")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False, help_text="Archived news are hidden from public views")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Default manager: only active (non-archived) news
    objects = ActiveNewsManager()
    # Fallback manager: all news including archived
    all_objects = models.Manager()
    
    class Meta:
        verbose_name_plural = 'News'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

