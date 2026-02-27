from django.urls import path
from . import views

urlpatterns = [
    path('', views.disclosure_list, name='disclosure'),
]
