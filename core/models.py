from django.db import models
from ckeditor.fields import RichTextField


class Banner(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=100, blank=True)
    button_link = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    status = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        ordering = ['order']
        verbose_name = 'Banner'
        verbose_name_plural = 'Banners'

    def __str__(self):
        return self.title


class Popup(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='popups/', blank=True, null=True)
    button_link = models.CharField(max_length=300, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        verbose_name = 'Popup'
        verbose_name_plural = 'Popups'

    def __str__(self):
        return self.title


class About(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='about/')
    vision = RichTextField(blank=True)
    mission = RichTextField(blank=True)

    class Meta:
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return self.title


class ContactInfo(models.Model):
    address = models.TextField()
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    google_map_embed_code = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Contact Info'
        verbose_name_plural = 'Contact Info'

    def __str__(self):
        return f"Contact Info"


class SocialMedia(models.Model):
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Social Media'
        verbose_name_plural = 'Social Media'

    def __str__(self):
        return "Social Media Links"


class SiteSettings(models.Model):
    """Singleton model — only one record allowed. Controls site-wide appearance."""
    school_name = models.CharField(max_length=200, default='Little Flower Children School')
    tagline = models.CharField(max_length=300, blank=True, default='Excellence in Education')
    short_name = models.CharField(max_length=20, default='LFCS', help_text='Short name shown in navbar e.g. LFCS')
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Navbar logo image')
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Browser tab icon (32×32 .ico or .png)')
    established_year = models.CharField(max_length=10, default='2000')
    primary_color = models.CharField(max_length=10, default='#1a3c6b', help_text='Hex code e.g. #1a3c6b')
    secondary_color = models.CharField(max_length=10, default='#e8a020', help_text='Hex code e.g. #e8a020')
    footer_text = models.CharField(max_length=400, blank=True, help_text='Short text shown in footer')

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return f"{self.school_name} – Site Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton: always use pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
