from django.urls import path
from . import views

urlpatterns = [
    path('curriculum/', views.curriculum, name='curriculum'),
    path('fees/', views.fee_structure, name='fee_structure'),
    path('books/', views.book_list, name='book_list'),
    path('calendar/', views.academic_calendar, name='academic_calendar'),
    path('admission/', views.admission_process, name='admission_process'),
]
