from django.contrib import admin
from import_export.admin import ExportActionMixin
from .models import Enquiry, CareerApplication


@admin.register(Enquiry)
class EnquiryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'class_interested', 'date', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'phone', 'email')
    list_editable = ('status',)
    readonly_fields = ('name', 'phone', 'email', 'message', 'class_interested', 'date')


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'applied_for', 'qualification', 'phone', 'email', 'applied_on')
    search_fields = ('name', 'applied_for')
    list_filter = ('applied_for',)
