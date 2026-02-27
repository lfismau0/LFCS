from django.db import models


class TC(models.Model):
    student_name = models.CharField(max_length=200)
    student_class = models.CharField(max_length=50)
    father_name = models.CharField(max_length=200)
    admission_no = models.CharField(max_length=50, unique=True)
    tc_number = models.CharField(max_length=50, unique=True)
    pdf_upload = models.FileField(upload_to='tc/pdfs/', blank=True, null=True)
    issue_date = models.DateField()

    class Meta:
        verbose_name = 'Transfer Certificate'
        verbose_name_plural = 'Transfer Certificates'

    def __str__(self):
        return f"{self.student_name} - {self.admission_no}"
