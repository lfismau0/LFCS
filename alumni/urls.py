from django.urls import path
from . import views

urlpatterns = [
    path('', views.alumni_list, name='alumni'),
]
