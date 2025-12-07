from django.db import models


class AboutPage(models.Model):
    PAGE_CHOICES = [
        ('mission', 'Mission'),
        ('vision', 'Vision'),
        ('principal', "Principal's Message"),
    ]
    
    page_type = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Pages'
    
    def __str__(self):
        return self.get_page_type_display()



