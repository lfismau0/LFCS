from django.utils import timezone
from core.models import ContactInfo, SocialMedia, SiteSettings
from notice_board.models import Notice


def global_context(request):
    contact = ContactInfo.objects.first()
    social = SocialMedia.objects.first()
    site_settings = SiteSettings.get_settings()
    today = timezone.now().date()
    important_notices = Notice.objects.filter(
        is_important=True,
        publish_date__lte=today
    ).exclude(expiry_date__lt=today)[:3]

    return {
        'contact': contact,
        'social': social,
        'site_settings': site_settings,
        'important_notices': important_notices,
    }
