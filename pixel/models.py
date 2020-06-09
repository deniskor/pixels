from django.db import models


class Rectangle(models.Model):
    width = models.IntegerField(default=20)
    height = models.IntegerField(default=20)


class Pixel(models.Model):
    rect = models.ForeignKey(Rectangle, on_delete=models.CASCADE, default=0)
    x = models.IntegerField()
    y = models.IntegerField()
    color = models.CharField(max_length=6, default='ffffff')

