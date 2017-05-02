from django.db import models

# Create your models here.

class ScreenPlay(models.Model):
    case_no = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    filling_unit = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    result = models.CharField(max_length=32)
    case_type = models.CharField(max_length=16, default="unknown")
    region = models.CharField(max_length=32, null=True)
    case_time_start = models.CharField(max_length=32, null=True)
    case_time_end = models.CharField(max_length=32, null=True)
    case_time = models.CharField(max_length=32, null=True)
    case_url = models.URLField(max_length=256)
    path_url = models.URLField(max_length=256)

    class Meta:
        db_table = "screenplay"

    def __str__(self):
        return self.name
