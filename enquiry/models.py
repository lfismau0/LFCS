from django.db import models
from django.utils import timezone


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('replied', 'Replied'),
        ('resolved', 'Resolved'),
    ]
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()
    class_interested = models.CharField(max_length=50, blank=True)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Enquiry'
        verbose_name_plural = 'Enquiries'

    def __str__(self):
        return f"{self.name} - {self.date.strftime('%d %b %Y')}"


class CareerApplication(models.Model):
    name = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=100, blank=True)
    resume_upload = models.FileField(upload_to='career/resumes/')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    applied_for = models.CharField(max_length=200)
    applied_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-applied_on']
        verbose_name = 'Career Application'
        verbose_name_plural = 'Career Applications'

    def __str__(self):
        return f"{self.name} - {self.applied_for}"
