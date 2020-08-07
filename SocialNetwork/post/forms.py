from django import forms
from django.db import transaction
from .models import *

class PostForm(forms.ModelForm):
   
    
    class Meta:
        model = Post
        exclude = ('user','post_date',)

    
