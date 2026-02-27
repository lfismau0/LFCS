from django.contrib import admin
from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'department', 'experience')
    list_filter = ('department',)
    search_fields = ('name', 'designation')
