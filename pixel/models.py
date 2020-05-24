from django.db import models


# Create your models here.
class Pixel(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=6, default='ffffff')

