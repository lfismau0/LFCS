from django.contrib import admin
from .models import House, HouseLeader


class HouseLeaderInline(admin.TabularInline):
    model = HouseLeader
    extra = 1


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('house_name', 'color')
    inlines = [HouseLeaderInline]


@admin.register(HouseLeader)
class HouseLeaderAdmin(admin.ModelAdmin):
    list_display = ('house', 'head_boy', 'head_girl', 'year')
    list_filter = ('house', 'year')
