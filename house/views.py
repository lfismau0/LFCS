from django.shortcuts import render
from .models import House


def house_view(request):
    houses = House.objects.prefetch_related('leaders').all()
    return render(request, 'house/house.html', {'houses': houses})
