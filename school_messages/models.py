from django.db import models
from ckeditor.fields import RichTextField


class DirectorMessage(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='messages/director/')
    message = RichTextField()
    designation = models.CharField(max_length=200, default='Director')

    class Meta:
        verbose_name = "Director's Message"
        verbose_name_plural = "Director's Message"

    def __str__(self):
        return self.name


class PrincipalMessage(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='messages/principal/')
    message = RichTextField()
    qualification = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Principal's Message"
        verbose_name_plural = "Principal's Message"

    def __str__(self):
        return self.name
