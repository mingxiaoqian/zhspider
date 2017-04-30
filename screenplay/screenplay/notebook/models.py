from django.db import models

# Create your models here.

class ScreenPlay(models.Model):
    case_no = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=64)
    filling_unit = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    result = models.CharField(max_length=32)
    region = models.CharField(max_length=32)
    case_url = models.URLField(max_length=256)
    path_url = models.URLField(max_length=256)
    case_time = models.CharField(max_length=32)


    def __str__(self):
        return self.name
