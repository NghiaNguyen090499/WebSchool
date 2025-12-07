#!/usr/bin/env python
"""Quick script to check crawled data"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_website.settings')
django.setup()

from django.utils import timezone
from news.models import News, Category
from events.models import Event
from gallery.models import Album
from about.models import AboutPage

print("=" * 60)
print("DATABASE SUMMARY")
print("=" * 60)

# News
news_count = News.objects.count()
news_with_images = News.objects.exclude(thumbnail__isnull=True).exclude(thumbnail='').count()
print(f"\n📰 NEWS: {news_count} articles")
print(f"   - With images: {news_with_images}")
print(f"   - Without images: {news_count - news_with_images}")

if news_count > 0:
    latest = News.objects.order_by('-created_at')[:3]
    print("\n   Latest articles:")
    for n in latest:
        has_img = "✓" if n.thumbnail else "✗"
        print(f"   {has_img} {n.title[:60]}...")

# Categories
categories = Category.objects.all()
print(f"\n📂 CATEGORIES: {categories.count()}")
for cat in categories:
    count = News.objects.filter(category=cat).count()
    print(f"   - {cat.name}: {count} articles")

# Events
events_count = Event.objects.count()
events_with_images = Event.objects.exclude(image__isnull=True).exclude(image='').count()
print(f"\n📅 EVENTS: {events_count} events")
print(f"   - With images: {events_with_images}")
print(f"   - Without images: {events_count - events_with_images}")

if events_count > 0:
    upcoming = Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:3]
    print("\n   Upcoming events:")
    for e in upcoming:
        has_img = "✓" if e.image else "✗"
        print(f"   {has_img} {e.title[:60]}... ({e.date})")

# Albums
albums_count = Album.objects.count()
print(f"\n📸 GALLERY ALBUMS: {albums_count}")
if albums_count > 0:
    for album in Album.objects.all()[:5]:
        photo_count = album.photos.count()
        print(f"   - {album.name}: {photo_count} photos")

# About Pages
about_pages = AboutPage.objects.all()
print(f"\n📖 ABOUT PAGES: {about_pages.count()}")
for page in about_pages:
    has_img = "✓" if page.image else "✗"
    print(f"   {has_img} {page.get_page_type_display()}: {page.title[:50]}...")

print("\n" + "=" * 60)
print("✅ Data check complete!")
print("=" * 60)

