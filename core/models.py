from django.db import models


class CoreValue(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="Icon class name (e.g., 'fas fa-graduation-cap')")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Core Value'
        verbose_name_plural = 'Core Values'
    
    def __str__(self):
        return self.title


class Statistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()
    icon = models.CharField(max_length=100, help_text="Icon class name")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'
    
    def __str__(self):
        return f"{self.label}: {self.value}"



