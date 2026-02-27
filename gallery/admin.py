from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages as django_messages
from .models import Album, Photo, Video


# ─────────────────────────────────────────────────────────────────────────────
# PHOTO INLINE  (with thumbnail + bulk upload support)
# ─────────────────────────────────────────────────────────────────────────────
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    fields = ('thumb_preview', 'image', 'caption')
    readonly_fields = ('thumb_preview',)

    def thumb_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:6px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return format_html('<span style="color:#aaa;font-size:.8rem;">Not saved yet</span>')
    thumb_preview.short_description = '👁'


# ─────────────────────────────────────────────────────────────────────────────
# ALBUM ADMIN  (with bulk upload view)
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('cover_thumb', 'album_name', 'photo_count', 'created_at')
    list_display_links = ('cover_thumb', 'album_name')
    search_fields = ('album_name',)
    list_per_page = 20
    inlines = [PhotoInline]

    fieldsets = (
        ('Album Info', {
            'fields': ('album_name', 'cover_image'),
            'description': (
                '<div class="bulk-upload-note">'
                '💡 <strong>Bulk Upload Tip:</strong> After saving the album, scroll down to the Photos section. '
                'Click <strong>"Add another Photo"</strong> and hold <strong>Ctrl (or Cmd on Mac)</strong> '
                'while clicking in the file picker to select multiple images at once. '
                'Or use the <a href="bulk-upload/">📤 Bulk Upload</a> button for even faster uploads.'
                '</div>'
            ),
        }),
    )

    def cover_thumb(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width:80px;height:55px;object-fit:cover;border-radius:8px;border:2px solid #dee2e6;" />',
                obj.cover_image.url
            )
        return format_html('<div style="width:80px;height:55px;background:#f0f0f0;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#aaa;font-size:.7rem;">No cover</div>')
    cover_thumb.short_description = '📷 Cover'

    def photo_count(self, obj):
        count = obj.photos.count()
        color = '#28a745' if count > 0 else '#dc3545'
        return format_html(
            '<span style="background:{};color:#fff;padding:.2rem .7rem;border-radius:20px;font-weight:600;font-size:.8rem;">{} Photos</span>',
            color, count
        )
    photo_count.short_description = 'Photos'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:album_id>/bulk-upload/', self.admin_site.admin_view(self.bulk_upload_view), name='gallery_album_bulk_upload'),
        ]
        return custom_urls + urls

    def bulk_upload_view(self, request, album_id):
        from django.shortcuts import get_object_or_404, render
        from django.contrib.auth.decorators import login_required

        album = get_object_or_404(Album, pk=album_id)

        if request.method == 'POST':
            files = request.FILES.getlist('images')
            if not files:
                django_messages.warning(request, 'No files were uploaded.')
            else:
                created = 0
                for f in files:
                    Photo.objects.create(album=album, image=f, caption='')
                    created += 1
                django_messages.success(request, f'✅ Successfully uploaded {created} photo(s) to "{album.album_name}"!')
                return HttpResponseRedirect(f'/admin/gallery/album/{album_id}/change/')

        context = {
            **self.admin_site.each_context(request),
            'album': album,
            'title': f'Bulk Upload Photos — {album.album_name}',
            'opts': self.model._meta,
        }
        return render(request, 'admin/gallery/bulk_upload.html', context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = f'/admin/gallery/album/{object_id}/bulk-upload/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


# ─────────────────────────────────────────────────────────────────────────────
# PHOTO ADMIN
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'album', 'caption')
    list_filter = ('album',)
    list_per_page = 30
    search_fields = ('caption', 'album__album_name')

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:70px;height:50px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return '—'
    thumb.short_description = '📷'


# ─────────────────────────────────────────────────────────────────────────────
# VIDEO ADMIN
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'created_at')
    list_display_links = ('thumb', 'title')
    search_fields = ('title',)
    list_per_page = 20
    fieldsets = (
        ('Video Info', {'fields': ('title', 'youtube_link', 'description')}),
        ('Thumbnail (optional)', {'fields': ('thumbnail',), 'classes': ('collapse',)}),
    )

    def thumb(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:6px;" />', obj.thumbnail.url)
        return format_html('<div style="width:80px;height:50px;background:#1a1a2e;border-radius:6px;display:flex;align-items:center;justify-content:center;"><span style="color:#fff;font-size:1.2rem;">▶</span></div>')
    thumb.short_description = '🎬'
