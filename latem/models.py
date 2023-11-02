from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    telephone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    isAdmin=models.BooleanField(default=False)
