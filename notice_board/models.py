from django.db import models
from django.utils import timezone


class Notice(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='notices/pdfs/', blank=True, null=True)
    publish_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    is_important = models.BooleanField(default=False, verbose_name='Pin / Important')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_important', '-publish_date']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title

    @property
    def is_active(self):
        today = timezone.now().date()
        if self.expiry_date and today > self.expiry_date:
            return False
        return True
