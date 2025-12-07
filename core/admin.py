from django.contrib import admin
from .models import CoreValue, Statistic


@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']
    search_fields = ['title']


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ['label', 'value', 'order']
    list_editable = ['order', 'value']



