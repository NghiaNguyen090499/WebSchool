"""
Django Sitemap Configuration for MIS Website
Generates XML sitemap for search engine optimization
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from news.models import News
from events.models import Event
from about.models import AboutPage
from core.models import TrainingProgram
from gallery.models import Album


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'core:home',
            'core:training_programs',
            'core:student_life',
            'core:student_spotlight',
            'core:pillars',
            'core:facilities',
            'core:podcasts',
            'contact:contact',
            'admissions:list',
            'news:list',
            'events:list',
            'gallery:list',
        ]

    def location(self, item):
        return reverse(item)


class AboutPageSitemap(Sitemap):
    """Sitemap for About pages"""
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return [
            'about:academics',
            'about:preschool',
            'about:primary',
            'about:middle',
            'about:high',
            'about:mission',
            'about:vision',
            'about:principal',
            'about:culture',
            'about:strengths',
            'about:structure',
            'about:strategy',
            'about:strategy_2025_2028',
            'about:vision_2033',
            'about:future_ai',
            'about:whymis',
            'about:steam',
            'about:robotics',
            'about:liberal',
            'about:happiness',
            'about:boarding',
            'about:overview_math',
            'about:overview_literature',
            'about:overview_english',
            'about:overview_chinese',
            'about:tnst',
            'about:lifeskills',
            'about:creative_movement',
            'about:schedule_2026',
            'about:schedule_hd_2026',
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    """Sitemap for News articles"""
    changefreq = 'daily'
    priority = 0.6

    def items(self):
        return (
            News.objects.exclude(slug__isnull=True)
            .exclude(slug='')
            .order_by('-created_at')[:100]
        )

    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


class EventSitemap(Sitemap):
    """Sitemap for Events"""
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Event.objects.all().order_by('-date')[:50]

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return obj.get_absolute_url()


class TrainingProgramSitemap(Sitemap):
    """Sitemap for Training Programs"""
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return TrainingProgram.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class GallerySitemap(Sitemap):
    """Sitemap for Gallery Albums"""
    changefreq = 'weekly'
    priority = 0.4

    def items(self):
        return (
            Album.objects.exclude(slug__isnull=True)
            .exclude(slug='')
            .order_by('-created_at')[:30]
        )

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()


# Sitemap dictionary for urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'about': AboutPageSitemap,
    'news': NewsSitemap,
    'events': EventSitemap,
    'training': TrainingProgramSitemap,
    'gallery': GallerySitemap,
}
