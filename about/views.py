from django.shortcuts import render, get_object_or_404
from .models import AboutPage


def mission(request):
    page = get_object_or_404(AboutPage, page_type='mission')
    return render(request, 'about/page.html', {'page': page})


def vision(request):
    page = get_object_or_404(AboutPage, page_type='vision')
    return render(request, 'about/page.html', {'page': page})


def principal_message(request):
    page = get_object_or_404(AboutPage, page_type='principal')
    return render(request, 'about/page.html', {'page': page})



