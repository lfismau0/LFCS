from django.contrib import admin
from .models import PublicDisclosure


@admin.register(PublicDisclosure)
class PublicDisclosureAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'publish_date')
    list_filter = ('category',)
    search_fields = ('title',)
