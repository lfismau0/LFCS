from django.db import models


class Corner(models.Model):
    CATEGORY_CHOICES = [
        ('student', 'Student Corner'),
        ('teacher', 'Teacher Corner'),
        ('parent', 'Parent Corner'),
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    file_upload = models.FileField(upload_to='corner/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Corner Item'
        verbose_name_plural = 'Corner Items'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
