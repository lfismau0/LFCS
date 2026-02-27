from django.shortcuts import render
from .models import SchoolCaptain


def captain_view(request):
    captains = SchoolCaptain.objects.all()
    return render(request, 'captain/captain.html', {'captains': captains})
