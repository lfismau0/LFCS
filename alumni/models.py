from django.db import models


class Alumni(models.Model):
    name = models.CharField(max_length=200)
    batch = models.CharField(max_length=10)
    profession = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='alumni/', blank=True, null=True)
    achievement = models.TextField(blank=True)

    class Meta:
        ordering = ['-batch']
        verbose_name = 'Alumni'
        verbose_name_plural = 'Alumni'

    def __str__(self):
        return f"{self.name} (Batch {self.batch})"
