from django.urls import path
from . import views

urlpatterns = [
    path('<str:category>/', views.corner_view, name='corner'),
]
