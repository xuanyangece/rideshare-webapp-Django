from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta, datetime

def emptylist():
    return [];

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #email and name in User
    driver = models.BooleanField(default=False)
    vehicle = models.CharField(max_length=20, blank=True)
    plate = models.CharField(max_length=10, blank=True)
    capacity = models.IntegerField(default=1, validators=[MaxValueValidator(200),MinValueValidator(1)])
    special = models.CharField(max_length=200, blank=True, default='')
    
class Ride(models.Model):
    status = models.CharField(max_length=10, default='open')
    destination = models.CharField(max_length=50, blank=False)
    arrivaldate = models.DateTimeField()
    passenger = models.IntegerField(validators=[MaxValueValidator(200),MinValueValidator(1)])
    sharable = models.BooleanField(default=False)
    vehicle = models.CharField(max_length=20, blank=True)
    special = models.CharField(max_length=200, blank=True)
    driver_id = models.IntegerField(default=-1, blank=True)
    rider_id = models.IntegerField(default=-1, blank=False)
    sharer_id = ArrayField(models.IntegerField(), default=emptylist)
    sharer_passenger = ArrayField(models.IntegerField(), default=emptylist)
    total_psg = models.IntegerField(validators=[MaxValueValidator(200),MinValueValidator(1)], default=0)
