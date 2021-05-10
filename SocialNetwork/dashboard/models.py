from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', unique = True)
    date_of_birth = models.DateField(null = True)
    gender = models.CharField(max_length=10, default='Male', choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')))
    user_image = models.ImageField(default="user.jpg", null= True)
    bad_word_count = models.IntegerField(default=0)
    bad_msg_count = models.IntegerField(default=0)
    nude_count = models.IntegerField(default=0)

    
    def __str__(self):
        return self.username
