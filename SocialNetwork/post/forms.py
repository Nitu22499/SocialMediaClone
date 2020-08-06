from django import forms
from django.db import transaction
from .models import *

class PostForm(forms.ModelForm):
    post_body = forms.CharField(label='Message', widget=forms.TextInput(attrs={'placeholder':'Write Something'}))
    class Meta:
        model = Post
        exclude = ('user','post_date',)

    
