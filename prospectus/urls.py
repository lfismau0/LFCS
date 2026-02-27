from django.urls import path
from . import views

urlpatterns = [
    path('', views.prospectus_view, name='prospectus'),
]
