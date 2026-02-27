from django.shortcuts import render
from .models import PublicDisclosure
from core.models import ContactInfo


def disclosure_list(request):
    disclosures = PublicDisclosure.objects.all()
    contact = ContactInfo.objects.first()
    return render(request, 'disclosure/disclosure.html', {
        'disclosures': disclosures,
        'contact': contact,
    })
