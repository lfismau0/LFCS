from django.contrib import admin
from .models import DirectorMessage, PrincipalMessage


@admin.register(DirectorMessage)
class DirectorMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')


@admin.register(PrincipalMessage)
class PrincipalMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'qualification')
