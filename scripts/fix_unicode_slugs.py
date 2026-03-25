# -*- coding: utf-8 -*-
"""Fix unicode slugs in News and Category models - convert to ASCII."""
import os, sys, unicodedata

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_website.settings")

import django
django.setup()

from django.utils.text import slugify
from news.models import News, Category


def vietnamese_to_ascii(text):
    """Remove Vietnamese diacritics and convert to ASCII-friendly text."""
    vietnamese_map = {
        'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a',
        'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a',
        'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a',
        'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e',
        'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e',
        'i': 'i', 'i': 'i', 'i': 'i', 'i': 'i', 'i': 'i',
        'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o',
        'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o',
        'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o',
        'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u',
        'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u',
        'y': 'y', 'y': 'y', 'y': 'y', 'y': 'y', 'y': 'y',
        'd': 'd',
    }
    # Use proper Unicode normalization approach
    # First decompose, then strip combining marks
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = ''
    for char in nfkd:
        if char == '\u0111':  # d
            ascii_text += 'd'
        elif char == '\u0110':  # D
            ascii_text += 'D'
        elif unicodedata.category(char) == 'Mn':  # combining mark
            continue
        else:
            ascii_text += char
    return ascii_text


def make_ascii_slug(text, max_length=200):
    """Create ASCII-only slug from Vietnamese text."""
    ascii_text = vietnamese_to_ascii(text)
    slug = slugify(ascii_text)
    if not slug:
        import hashlib
        slug = hashlib.md5(text.encode()).hexdigest()[:12]
    return slug[:max_length]


def make_unique_slug(slug, model_class, exclude_pk=None):
    """Ensure slug is unique by appending a number if needed."""
    original_slug = slug
    counter = 1
    qs = model_class.objects.filter(slug=slug)
    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)
    while qs.exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
        qs = model_class.objects.filter(slug=slug)
        if exclude_pk:
            qs = qs.exclude(pk=exclude_pk)
    return slug


def has_unicode(text):
    """Check if text contains non-ASCII characters."""
    try:
        text.encode('ascii')
        return False
    except UnicodeEncodeError:
        return True


def run():
    print("=" * 70)
    print("  FIX UNICODE SLUGS -> ASCII")
    print("=" * 70)

    # Fix News slugs
    news_fixed = 0
    for news in News.objects.all():
        if has_unicode(news.slug):
            old_slug = news.slug
            new_slug = make_ascii_slug(news.title)
            new_slug = make_unique_slug(new_slug, News, exclude_pk=news.pk)
            News.objects.filter(pk=news.pk).update(slug=new_slug)
            news_fixed += 1
            print(f"  News: {old_slug[:50]}  ->  {new_slug[:50]}")

    # Fix Category slugs
    cat_fixed = 0
    for cat in Category.objects.all():
        if has_unicode(cat.slug):
            old_slug = cat.slug
            new_slug = make_ascii_slug(cat.name)
            new_slug = make_unique_slug(new_slug, Category, exclude_pk=cat.pk)
            Category.objects.filter(pk=cat.pk).update(slug=new_slug)
            cat_fixed += 1
            print(f"  Category: {old_slug[:40]}  ->  {new_slug[:40]}")

    print(f"\nDone! Fixed {news_fixed} news slugs, {cat_fixed} category slugs.")


if __name__ == "__main__":
    run()
