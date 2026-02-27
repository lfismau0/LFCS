from django.contrib import admin
from .models import TC


@admin.register(TC)
class TCAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'admission_no', 'tc_number', 'student_class', 'issue_date')
    search_fields = ('student_name', 'admission_no', 'tc_number')
    list_filter = ('issue_date',)
