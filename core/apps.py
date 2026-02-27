from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        """Patch the default admin site to inject stats into the dashboard."""
        from django.contrib import admin

        _original_index = admin.site.__class__.index

        def patched_index(self, request, extra_context=None):
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
            return _original_index(self, request, extra_context)

        admin.site.__class__.index = patched_index
