from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField(max_length=10, default='Male', choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')))
    user_image = models.ImageField(upload_to ='documents/', null= True)
    

    def __str__(self):
        return self.first_name