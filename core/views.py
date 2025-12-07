from django.shortcuts import render
from django.utils import timezone
from news.models import News, Category
from events.models import Event
from gallery.models import Album, Photo
from .models import CoreValue, Statistic


def home(request):
    """Homepage view with all sections"""
    context = {
        'core_values': CoreValue.objects.all()[:8],  # Hiển thị tất cả 8 giá trị cốt lõi
        'statistics': Statistic.objects.all()[:4],
        'featured_news': News.objects.filter(is_featured=True).first(),
        'recent_news': News.objects.filter(is_featured=False)[:3],
        'upcoming_events': Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:3],
        'albums': Album.objects.all()[:6],
    }
    return render(request, 'core/home.html', context)

