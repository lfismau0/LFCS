from django.urls import path
from . import views

urlpatterns = [
    path('', views.enquiry_view, name='enquiry'),
    path('career/', views.career_view, name='career'),
]
