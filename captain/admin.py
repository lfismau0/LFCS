from django.contrib import admin
from .models import SchoolCaptain


@admin.register(SchoolCaptain)
class SchoolCaptainAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_class', 'year')
    list_filter = ('year',)
