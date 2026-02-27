from django.shortcuts import render
from django.utils import timezone
from .models import Notice


def notice_list(request):
    today = timezone.now().date()
    notices = Notice.objects.filter(publish_date__lte=today).exclude(expiry_date__lt=today)
    pinned = notices.filter(is_important=True)
    regular = notices.filter(is_important=False)
    return render(request, 'notice_board/notices.html', {
        'pinned': pinned, 'regular': regular
    })
