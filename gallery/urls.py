from django.urls import path
from . import views

urlpatterns = [
    path('photos/', views.photo_gallery, name='photo_gallery'),
    path('photos/<int:pk>/', views.album_detail, name='album_detail'),
    path('videos/', views.video_gallery, name='video_gallery'),
]
