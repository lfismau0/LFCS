from django.db import models


class SchoolCaptain(models.Model):
    name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50, verbose_name='Class')
    photo = models.ImageField(upload_to='captain/')
    message = models.TextField(blank=True)
    year = models.CharField(max_length=10)

    class Meta:
        ordering = ['-year']
        verbose_name = 'School Captain'
        verbose_name_plural = 'School Captains'

    def __str__(self):
        return f"{self.name} ({self.year})"
