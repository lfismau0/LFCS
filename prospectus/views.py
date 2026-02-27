from django.shortcuts import render
from .models import Prospectus


def prospectus_view(request):
    items = Prospectus.objects.all()
    return render(request, 'prospectus/prospectus.html', {'items': items})
