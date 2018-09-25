from django.db import models

# from django.utils import timezone


# Create your models here.
class Room(models.Model):
    room_number = models.CharField(max_length=200)
    seats = models.IntegerField()
    window = models.BooleanField()
    computer = models.BooleanField()
    monitor = models.BooleanField()
    floor = models.IntegerField()
    is_reserved = models.BooleanField()
