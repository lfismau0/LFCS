from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Banner, Popup, About, ContactInfo, SocialMedia
from notice_board.models import Notice
from facilities.models import Facility
from school_messages.models import DirectorMessage, PrincipalMessage
from gallery.models import Album, Video
from enquiry.models import Enquiry
from enquiry.forms import EnquiryForm


def home(request):
    today = timezone.now().date()
    banners = Banner.objects.filter(status=True)
    popup = Popup.objects.filter(
        status=True, start_date__lte=today, end_date__gte=today
    ).first()
    notices = Notice.objects.filter(publish_date__lte=today).exclude(
        expiry_date__lt=today
    )[:6]
    facilities = Facility.objects.all()[:6]
    albums = Album.objects.all()[:4]
    videos = Video.objects.all()[:3]
    director = DirectorMessage.objects.first()
    principal = PrincipalMessage.objects.first()
    about = About.objects.first()
    form = EnquiryForm()

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/home.html', {
                'banners': banners, 'popup': popup, 'notices': notices,
                'facilities': facilities, 'albums': albums, 'videos': videos,
                'director': director, 'principal': principal, 'about': about,
                'form': EnquiryForm(), 'success': True,
            })

    return render(request, 'core/home.html', {
        'banners': banners, 'popup': popup, 'notices': notices,
        'facilities': facilities, 'albums': albums, 'videos': videos,
        'director': director, 'principal': principal, 'about': about,
        'form': form,
    })


def about_view(request):
    about = About.objects.first()
    return render(request, 'core/about.html', {'about': about})


def contact_view(request):
    contact = ContactInfo.objects.first()
    form = EnquiryForm()
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            form = EnquiryForm()
            return render(request, 'core/contact.html', {'contact': contact, 'form': form, 'success': True})
    return render(request, 'core/contact.html', {'contact': contact, 'form': form})
