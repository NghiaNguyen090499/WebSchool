from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Album, Photo


def gallery_list(request):
    """List all albums"""
    albums = Album.objects.annotate(photo_count=Count('photos'))
    context = {
        'albums': albums,
    }
    return render(request, 'gallery/list.html', context)


def album_detail(request, slug):
    """Album detail with photos - limited to 20 images"""
    album = get_object_or_404(Album, slug=slug)
    photos_qs = album.photos.exclude(image='').exclude(image__isnull=True)
    total_photos = photos_qs.count()

    paginator = Paginator(photos_qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'album': album,
        'photos': page_obj,
        'page_obj': page_obj,
        'total_photos': total_photos,
        'page_count': len(page_obj.object_list),
    }
    return render(request, 'gallery/album_detail.html', context)







