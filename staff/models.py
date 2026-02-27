from django.db import models


class Staff(models.Model):
    DEPARTMENT_CHOICES = [
        ('management', 'Management'),
        ('science', 'Science'),
        ('maths', 'Mathematics'),
        ('english', 'English'),
        ('social', 'Social Studies'),
        ('hindi', 'Hindi'),
        ('computer', 'Computer Science'),
        ('arts', 'Arts & Crafts'),
        ('sports', 'Sports & PE'),
        ('administration', 'Administration'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    qualification = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='other')

    class Meta:
        ordering = ['department', 'name']
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'

    def __str__(self):
        return f"{self.name} - {self.designation}"
