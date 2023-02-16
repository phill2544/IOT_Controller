from django.db import models

# Create your models here.
from django.db import models

class Iot(models.Model):
    temp = models.FloatField(null = True)
    humid = models.FloatField(null = True)
    status_fan = models.BooleanField(null = True)
    status_lamp = models.BooleanField(null = True)
    status_water = models.BooleanField(null = True)
    adc = models.FloatField(null = True)
    class Meta:
        db_table = 'iot'