from django.contrib import admin
from .models import Curriculum, FeeStructure, BookList, AcademicCalendar, AdmissionProcess


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('class_name',)


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('class_name',)


@admin.register(BookList)
class BookListAdmin(admin.ModelAdmin):
    list_display = ('class_name',)


@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'year')


@admin.register(AdmissionProcess)
class AdmissionProcessAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
