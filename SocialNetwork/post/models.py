from django.db import models
from django.utils import timezone
from dashboard.models import User

# Create your models here.
class Post(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    post_image = models.FileField(upload_to='documents/',default=True)
    post_body = models.TextField(blank = True)
    post_date = models.DateTimeField(default=timezone.now)

