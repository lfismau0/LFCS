from django.contrib import admin
from .models import Prospectus


@admin.register(Prospectus)
class ProspectusAdmin(admin.ModelAdmin):
    list_display = ('year', 'description')
