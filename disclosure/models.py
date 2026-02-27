from django.db import models


class PublicDisclosure(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('financial', 'Financial'),
        ('academic', 'Academic'),
        ('infrastructure', 'Infrastructure'),
        ('cbse', 'CBSE'),
    ]
    title = models.CharField(max_length=300)
    document_pdf = models.FileField(upload_to='disclosure/pdfs/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    publish_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = 'Public Disclosure'
        verbose_name_plural = 'Public Disclosures'

    def __str__(self):
        return self.title
