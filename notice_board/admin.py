from django.contrib import admin
from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'expiry_date', 'is_important', 'is_active')
    list_editable = ('is_important',)
    list_filter = ('is_important',)
    search_fields = ('title',)

    def is_active(self, obj):
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'
