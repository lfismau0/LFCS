from django.db import models


class Facility(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='facilities/')
    icon = models.CharField(max_length=100, blank=True, help_text='Font Awesome icon class e.g. fa-book')

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
        return self.title
