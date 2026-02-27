from django.shortcuts import render
from .models import Curriculum, FeeStructure, BookList, AcademicCalendar, AdmissionProcess


def curriculum(request):
    items = Curriculum.objects.all()
    return render(request, 'academics/curriculum.html', {'items': items})


def fee_structure(request):
    items = FeeStructure.objects.all()
    return render(request, 'academics/fee_structure.html', {'items': items})


def book_list(request):
    items = BookList.objects.all()
    return render(request, 'academics/book_list.html', {'items': items})


def academic_calendar(request):
    items = AcademicCalendar.objects.all()
    return render(request, 'academics/calendar.html', {'items': items})


def admission_process(request):
    info = AdmissionProcess.objects.first()
    return render(request, 'academics/admission.html', {'info': info})
