from django.db import models
from ckeditor.fields import RichTextField


class Curriculum(models.Model):
    class_name = models.CharField(max_length=100)
    description = RichTextField(blank=True)
    pdf_upload = models.FileField(upload_to='academics/curriculum/', blank=True, null=True)

    class Meta:
        verbose_name = 'Curriculum'
        verbose_name_plural = 'Curricula'

    def __str__(self):
        return f"Curriculum - {self.class_name}"


class FeeStructure(models.Model):
    class_name = models.CharField(max_length=100)
    fee_details = RichTextField(blank=True)
    file_upload = models.FileField(upload_to='academics/fees/', blank=True, null=True, help_text="Upload an image (JPG/PNG) or PDF of the fee structure.")

    class Meta:
        verbose_name = 'Fee Structure'
        verbose_name_plural = 'Fee Structures'

    def __str__(self):
        return f"Fee Structure - {self.class_name}"


class BookList(models.Model):
    class_name = models.CharField(max_length=100)
    pdf_upload = models.FileField(upload_to='academics/booklists/')

    class Meta:
        verbose_name = 'Book List'
        verbose_name_plural = 'Book Lists'

    def __str__(self):
        return f"Book List - {self.class_name}"


class AcademicCalendar(models.Model):
    title = models.CharField(max_length=200)
    pdf_upload = models.FileField(upload_to='academics/calendars/')
    year = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Academic Calendar'
        verbose_name_plural = 'Academic Calendars'

    def __str__(self):
        return self.title


class AdmissionProcess(models.Model):
    description = RichTextField()
    file_upload = models.FileField(upload_to='academics/admission/', blank=True, null=True, help_text="Upload an image (JPG/PNG) or PDF for admission.")

    class Meta:
        verbose_name = 'Admission Process'
        verbose_name_plural = 'Admission Process'

    def __str__(self):
        return "Admission Process"
