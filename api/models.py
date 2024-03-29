"""Models"""
from datetime import datetime
from django.db import models


class Contest(models.Model):
    """Contest Model"""
    id = models.AutoField(primary_key=True)
    defTime = datetime(year=2000, month=1, day=1)
    name = models.CharField(max_length=255)
    startTime = models.DateTimeField(default=defTime)
    endTime = models.DateTimeField(default=defTime)
    site = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True)
