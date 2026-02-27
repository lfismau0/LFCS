from django.db import models


class Prospectus(models.Model):
    year = models.CharField(max_length=10)
    pdf_file = models.FileField(upload_to='prospectus/')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-year']
        verbose_name = 'Prospectus'
        verbose_name_plural = 'Prospectus'

    def __str__(self):
        return f"Prospectus {self.year}"
