from django.db import models
from django.utils import timezone
from dashboard.models import User
from django.urls import reverse_lazy, reverse

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    post_image = models.FileField(upload_to ='documents/')
    post_body = models.TextField(blank = True)
    post_date = models.DateTimeField(default=timezone.now)
    liked = models.ManyToManyField(User,default=None, blank=True, related_name="liked")

    class Meta:
        ordering = ['-post_date',]

    def get_absolute_url(self):
        return reverse_lazy('post:home')

    @property
    def num_of_likes(self):
        return self.liked.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.pk)
