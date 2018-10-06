# Create your models here.
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

class Contest(models.Model):
    defTime = datetime(year=2000,month=1,day=1)
    name = models.CharField(max_length=255)
    startTime = models.DateTimeField(default=defTime)
    endTime = models.DateTimeField(default=defTime)
    site = models.CharField(max_length=255)
