from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


class LFISAdminSite(AdminSite):
    """Custom admin site that injects live stats into the dashboard context."""

    site_header = '🎓 LFIS Admin Portal'
    site_title  = 'LFIS Admin'
    index_title = 'School Management Panel'

    def index(self, request, extra_context=None):
        """Inject model counts into the dashboard template context."""
        extra_context = extra_context or {}
        try:
            from staff.models import Staff
            extra_context['staff_count'] = Staff.objects.count()
        except Exception:
            extra_context['staff_count'] = '?'

        try:
            from notice_board.models import Notice
            extra_context['notice_count'] = Notice.objects.count()
        except Exception:
            extra_context['notice_count'] = '?'

        try:
            from gallery.models import Album
            extra_context['album_count'] = Album.objects.count()
        except Exception:
            extra_context['album_count'] = '?'

        try:
            from alumni.models import Alumni
            extra_context['alumni_count'] = Alumni.objects.count()
        except Exception:
            extra_context['alumni_count'] = '?'

        try:
            from enquiry.models import Enquiry
            extra_context['enquiry_count'] = Enquiry.objects.count()
        except Exception:
            extra_context['enquiry_count'] = '?'

        try:
            from facilities.models import Facility
            extra_context['facility_count'] = Facility.objects.count()
        except Exception:
            extra_context['facility_count'] = '?'

        return super().index(request, extra_context)


# Singleton instance
lfis_admin_site = LFISAdminSite(name='admin')
