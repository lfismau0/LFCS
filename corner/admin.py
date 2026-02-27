from django.contrib import admin
from .models import Corner


@admin.register(Corner)
class CornerAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)
