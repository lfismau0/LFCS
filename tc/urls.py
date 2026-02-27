from django.urls import path
from . import views

urlpatterns = [
    path('', views.tc_search, name='tc_search'),
]
