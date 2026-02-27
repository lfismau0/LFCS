from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from adminsortable2.admin import SortableAdminMixin
from import_export.admin import ExportActionMixin
from .models import Banner, Popup, About, ContactInfo, SocialMedia, SiteSettings


# ─────────────────────────────────────────────────────────────────────────────
# SITE SETTINGS  (Singleton Admin — auto-redirect to pk=1)
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏫  School Identity', {
            'fields': ('school_name', 'short_name', 'tagline', 'established_year'),
            'description': 'These values appear in the navbar, browser tab, and footer.',
        }),
        ('🖼️  Branding Assets', {
            'fields': ('logo', 'logo_preview', 'favicon', 'favicon_preview'),
            'description': 'Upload the school logo (recommended: 200×60px PNG). Favicon should be 32×32 .ico or .png.',
        }),
        ('🎨  Theme Colors', {
            'fields': ('primary_color', 'secondary_color'),
            'description': 'Enter hex color codes (e.g. #1a3c6b). Changes reflect site-wide via CSS variables.',
        }),
        ('📝  Footer', {
            'fields': ('footer_text',),
        }),
    )
    readonly_fields = ('logo_preview', 'favicon_preview')

    class Media:
        js = ('js/admin_color_preview.js',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:70px;border-radius:10px;border:2px solid #dee2e6;padding:4px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.1);" />',
                obj.logo.url
            )
        return format_html('<span style="color:#999;font-style:italic;">No logo uploaded yet</span>')
    logo_preview.short_description = 'Current Logo'

    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="width:32px;height:32px;border-radius:4px;" />', obj.favicon.url)
        return format_html('<span style="color:#999;font-style:italic;">No favicon uploaded yet</span>')
    favicon_preview.short_description = 'Current Favicon'

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('', self.admin_site.admin_view(self.singleton_redirect), name='core_sitesettings_changelist'),
        ]
        return custom + urls

    def singleton_redirect(self, request):
        """Always redirect to the single SiteSettings instance (pk=1)."""
        obj = SiteSettings.get_settings()
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk])
        )

    def get_object(self, request, object_id, from_field=None):
        SiteSettings.get_settings()
        return super().get_object(request, object_id, from_field)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, '✅ Site settings saved! Changes are now live on the website.')


# ─────────────────────────────────────────────────────────────────────────────
# BANNER
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('thumb', 'title', 'subtitle_short', 'order', 'status')
    list_editable = ('status', 'order')
    list_display_links = ('thumb', 'title')
    list_per_page = 20
    fieldsets = (
        (None, {'fields': ('title', 'subtitle', 'image', 'order', 'status')}),
        ('Button (optional)', {'fields': ('button_text', 'button_link'), 'classes': ('collapse',)}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" class="admin-thumb" title="{}" />',
                obj.image.url, obj.title
            )
        return '—'
    thumb.short_description = '📷'

    def subtitle_short(self, obj):
        return (obj.subtitle[:60] + '…') if obj.subtitle and len(obj.subtitle) > 60 else obj.subtitle
    subtitle_short.short_description = 'Subtitle'


# ─────────────────────────────────────────────────────────────────────────────
# POPUP
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Popup)
class PopupAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title', 'start_date', 'end_date', 'days_remaining', 'status')
    list_editable = ('status',)
    list_display_links = ('thumb', 'title')
    list_per_page = 20

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb" />', obj.image.url)
        return '—'
    thumb.short_description = '📷'

    def days_remaining(self, obj):
        from django.utils import timezone
        today = timezone.now().date()
        if obj.end_date < today:
            return format_html('<span class="badge badge-danger">Expired</span>')
        delta = (obj.end_date - today).days
        if delta <= 3:
            return format_html('<span class="badge badge-warning">{} days</span>', delta)
        return format_html('<span class="badge badge-success">{} days</span>', delta)
    days_remaining.short_description = 'Expires In'


# ─────────────────────────────────────────────────────────────────────────────
# ABOUT
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('thumb', 'title')
    list_display_links = ('thumb', 'title')
    fieldsets = (
        ('Main Content', {'fields': ('title', 'description', 'image')}),
        ('🎯 Vision & Mission', {'fields': ('vision', 'mission'), 'classes': ('collapse',)}),
    )

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" class="admin-thumb" />', obj.image.url)
        return '—'
    thumb.short_description = '📷'


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT INFO
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('address_short', 'phone', 'email', 'whatsapp')
    readonly_fields = ('map_preview',)
    fieldsets = (
        ('📍 Address & Contact', {'fields': ('address', 'phone', 'whatsapp', 'email')}),
        ('🗺️ Google Maps', {
            'fields': ('google_map_embed_code', 'map_preview'),
            'classes': ('collapse',),
            'description': 'Paste the full Google Maps embed iframe code here.',
        }),
    )

    def address_short(self, obj):
        return (obj.address[:80] + '…') if obj.address and len(obj.address) > 80 else obj.address
    address_short.short_description = 'Address'

    def map_preview(self, obj):
        if obj.google_map_embed_code:
            return format_html(
                '<div style="border-radius:10px;overflow:hidden;max-width:400px;">{}</div>',
                mark_safe(obj.google_map_embed_code)
            )
        if obj.address:
            return format_html(
                '<iframe src="https://maps.google.com/maps?q={}&output=embed" '
                'width="400" height="200" style="border:0;border-radius:10px;" allowfullscreen loading="lazy"></iframe>',
                obj.address
            )
        return format_html('<span style="color:#999;">No address set yet</span>')
    map_preview.short_description = 'Map Preview'

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, '✅ Contact information updated! Changes are live on the website.')


# ─────────────────────────────────────────────────────────────────────────────
# SOCIAL MEDIA
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('settings_name', 'fb_link', 'insta_link', 'youtube_link', 'twitter_link')
    list_display_links = ('settings_name',)
    fieldsets = (
        ('🌐 Social Media Links', {
            'fields': ('facebook_url', 'instagram_url', 'youtube_url', 'twitter_url'),
            'description': 'Enter full URLs including https://. Leave blank to hide the icon on the website.',
        }),
    )

    def settings_name(self, obj):
        return "⚙️ Edit Links"
    settings_name.short_description = 'Manage'

    def fb_link(self, obj):
        if obj.facebook_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#1877f2;font-weight:600;">'
                '<i class="fab fa-facebook"></i> Facebook</a>', obj.facebook_url
            )
        return format_html('<span style="color:#ccc;">—</span>')
    fb_link.short_description = 'Facebook'

    def insta_link(self, obj):
        if obj.instagram_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#e1306c;font-weight:600;">'
                '<i class="fab fa-instagram"></i> Instagram</a>', obj.instagram_url
            )
        return format_html('<span style="color:#ccc;">—</span>')
    insta_link.short_description = 'Instagram'

    def youtube_link(self, obj):
        if obj.youtube_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#ff0000;font-weight:600;">'
                '<i class="fab fa-youtube"></i> YouTube</a>', obj.youtube_url
            )
        return format_html('<span style="color:#ccc;">—</span>')
    youtube_link.short_description = 'YouTube'

    def twitter_link(self, obj):
        if obj.twitter_url:
            return format_html(
                '<a href="{}" target="_blank" style="color:#1da1f2;font-weight:600;">'
                '<i class="fab fa-twitter"></i> Twitter</a>', obj.twitter_url
            )
        return format_html('<span style="color:#ccc;">—</span>')
    twitter_link.short_description = 'Twitter'

    def has_add_permission(self, request):
        return not SocialMedia.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        messages.success(request, '✅ Social media links updated! Changes are live on the website.')
