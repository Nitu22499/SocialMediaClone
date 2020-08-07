from django.db import models
from django.utils import timezone
from dashboard.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    post_image = models.ImageField(upload_to ='documents/')
    post_body = models.TextField(blank = True)
    post_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
