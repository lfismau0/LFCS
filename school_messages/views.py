from django.shortcuts import render
from .models import DirectorMessage, PrincipalMessage


def director_message(request):
    director = DirectorMessage.objects.first()
    return render(request, 'school_messages/director.html', {'director': director})


def principal_message(request):
    principal = PrincipalMessage.objects.first()
    return render(request, 'school_messages/principal.html', {'principal': principal})
