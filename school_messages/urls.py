from django.urls import path
from . import views

urlpatterns = [
    path('director/', views.director_message, name='director_message'),
    path('principal/', views.principal_message, name='principal_message'),
]
