from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email=models.EmailField(verbose_name='Email Address', max_length=30, unique=True)

    REQUIRED_FIELDS=['user_name', 'first_name', 'last_name']
    USERNAME_FIELD= 'email'


    def get_username(self):
        return self.email

