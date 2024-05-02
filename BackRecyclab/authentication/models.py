from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)


    class Meta:
        db_table = 'auth_user'

class Collector(User):
    car_info = models.CharField(max_length=255)
    car_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'collector'


