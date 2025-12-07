from django.shortcuts import render, get_object_or_404
from .models import Album, Photo


def gallery_list(request):
    """List all albums"""
    albums = Album.objects.all()
    context = {
        'albums': albums,
    }
    return render(request, 'gallery/list.html', context)


def album_detail(request, slug):
    """Album detail with photos"""
    album = get_object_or_404(Album, slug=slug)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    return render(request, 'gallery/album_detail.html', context)



