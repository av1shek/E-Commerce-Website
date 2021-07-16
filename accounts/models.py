from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fname = models.CharField(max_length=90, default="default_value")
    lname = models.CharField(max_length=90, default="default_value")
    mobno = models.CharField(max_length=90, default="default_value")
    address = models.CharField(max_length=200, default="default_value")
    city = models.CharField(max_length=50, default="default_value")
    zip_code = models.CharField(max_length=50, default="default_value")
    state = models.CharField(max_length=50, default="default_value")

    def save(self):
        super().save()

    def __str__(self):
        return self.user.username