from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, Category


def news_list(request):
    """List all news with pagination"""
    news_list = News.objects.all()
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        news_list = news_list.filter(category=category)
    else:
        category = None
    
    paginator = Paginator(news_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'selected_category': category,
    }
    return render(request, 'news/list.html', context)


def news_detail(request, slug):
    """News detail page"""
    news = get_object_or_404(News, slug=slug)
    related_news = News.objects.filter(category=news.category).exclude(id=news.id)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/detail.html', context)



