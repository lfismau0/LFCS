from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', include('core.urls')),
    path('gallery/', include('gallery.urls')),
    path('notices/', include('notice_board.urls')),
    path('tc/', include('tc.urls')),
    path('disclosure/', include('disclosure.urls')),
    path('facilities/', include('facilities.urls')),
    path('messages/', include('school_messages.urls')),
    path('academics/', include('academics.urls')),
    path('corner/', include('corner.urls')),
    path('captain/', include('captain.urls')),
    path('house/', include('house.urls')),
    path('prospectus/', include('prospectus.urls')),
    path('alumni/', include('alumni.urls')),
    path('staff/', include('staff.urls')),
    path('enquiry/', include('enquiry.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'LFIS Admin Portal'
admin.site.site_title = 'LFIS Admin'
admin.site.index_title = 'School Management Panel'
