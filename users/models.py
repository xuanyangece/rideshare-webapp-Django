from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #email and name in User
    driver = models.BooleanField(default=False)
    vehicle = models.CharField(max_length=20, blank=True)
    plate = models.CharField(max_length=10, blank=True)
    capacity = models.IntegerField(default=1, validators=[MaxValueValidator(200),MinValueValidator(1)])
    special = models.CharField(max_length=200, blank=True)
    
