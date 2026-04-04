from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('viewer',   'Viewer'),
        ('analyst',  'Analyst'),
        ('admin',    'Admin'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='viewer')
    def __str__(self):
        return f"{self.username} ({self.role})"