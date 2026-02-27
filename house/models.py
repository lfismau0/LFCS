from django.db import models


class House(models.Model):
    house_name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='house/logos/', blank=True, null=True)

    class Meta:
        verbose_name = 'House'
        verbose_name_plural = 'Houses'

    def __str__(self):
        return self.house_name


class HouseLeader(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='leaders')
    head_boy = models.CharField(max_length=200)
    head_girl = models.CharField(max_length=200)
    vice_head_boy = models.CharField(max_length=200, blank=True)
    vice_head_girl = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='house/leaders/', blank=True, null=True)
    year = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'House Leader'
        verbose_name_plural = 'House Leaders'

    def __str__(self):
        return f"{self.house.house_name} Leaders - {self.year}"
