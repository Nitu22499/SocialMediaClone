from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
import random
import datetime

from dashboard.models import User


class UserSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'form-select'}))


    class Meta(UserCreationForm.Meta):
        model = User
        fields=('username','first_name','last_name','email','gender','date_of_birth','password1',)
        
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        print(user)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.gender = self.cleaned_data['gender']
        user.date_of_birth = self.cleaned_data['date_of_birth']
        user.save()
        print(user)
        return user


class EditProfileForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'autofocus'}))
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    gender = forms.CharField(widget=forms.Select(choices=(('MALE', 'MALE'), ('FEMALE', 'FEMALE')), attrs={'class':'formselect'}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta(UserChangeForm.Meta):
        model = User
        fields="_all_"