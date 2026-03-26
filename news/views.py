import re

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from .models import Category, News


def clean_excerpt(text):
    """Clean crawled excerpt by removing social share junk text."""
    if not text:
        return ""
    # Remove "Share on Facebook", "Share on Twitter" patterns
    text = re.sub(r'Share on (Facebook|Twitter|LinkedIn|Pinterest|Email)\s*', '', text, flags=re.IGNORECASE)
    # Remove standalone "Share" and "Tweet"
    text = re.sub(r'\b(Share|Tweet)\b\s*', '', text)
    # Clean up multiple whitespace/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def news_list(request):
    """List all news with pagination, search and category filter."""
    category_slug = request.GET.get('category')
    query = request.GET.get('q', '').strip()

    # Get category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        all_news = News.objects.filter(category=category)
    else:
        category = None
        all_news = News.objects.all()

    # Apply search query if provided
    if query:
        all_news = all_news.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query)
        )

    # Get hero article: first featured or first regular
    hero_article = all_news.filter(is_featured=True).first()
    if not hero_article:
        hero_article = all_news.first()

    # The template 'list.html' displays the hero article separately ONLY if there is no search query.
    # Therefore, we only exclude the hero article from the grid when there is no search query.
    # Other featured articles should just appear in the regular grid instead of being hidden.
    if hero_article and not query:
        regular_news = all_news.exclude(id=hero_article.id)
    else:
        regular_news = all_news

    # Paginate regular news
    paginator = Paginator(regular_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get popular categories (with article count, top 8)
    popular_categories = Category.objects.annotate(
        news_count=Count('news', filter=Q(news__is_archived=False))
    ).filter(news_count__gt=0).order_by('-news_count')[:8]

    context = {
        'hero_article': hero_article,
        'page_obj': page_obj,
        'categories': popular_categories,
        'all_categories': Category.objects.all(),
        'selected_category': category,
        'search_query': query,
        'total_news': all_news.count(),
    }
    return render(request, 'news/list.html', context)


def news_detail(request, slug):
    """News detail page"""
    # Use all_objects so archived articles are still viewable via direct URL
    news = get_object_or_404(News.all_objects, slug=slug)
    related_news = News.objects.filter(category=news.category).exclude(id=news.id)[:3]

    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/detail.html', context)
