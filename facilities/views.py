from django.shortcuts import render
from .models import Facility


def facility_list(request):
    facilities = Facility.objects.all()
    return render(request, 'facilities/facilities.html', {'facilities': facilities})
