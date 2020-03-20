from django.db import models

# Create your models here.

class Ride(models.Model):

    ride_id = models.AutoField(primary_key=True)
    ride_created_by = models.CharField(max_length=40)
    source = models.IntegerField()
    destination = models.IntegerField()
    timestamp = models.CharField(max_length=19,default='')
    riders_list = models.TextField(default='')

    def __str__(self):
        return str(self.ride_id)
