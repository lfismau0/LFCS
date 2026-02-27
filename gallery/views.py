from django.shortcuts import render, get_object_or_404
from .models import Album, Photo, Video


def photo_gallery(request):
    albums = Album.objects.all()
    return render(request, 'gallery/photo_gallery.html', {'albums': albums})


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk)
    photos = album.photos.all()
    return render(request, 'gallery/album_detail.html', {'album': album, 'photos': photos})


def video_gallery(request):
    videos = Video.objects.all()
    return render(request, 'gallery/video_gallery.html', {'videos': videos})
