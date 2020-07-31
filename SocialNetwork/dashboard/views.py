from django.contrib import messages, auth
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView,TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import UserSignUpForm

# Create your views here.

class Login(LoginView):
    template_name = 'dashboard/login.html'
    

class RegisterView(CreateView):
    
    
    model = User
    form_class = UserSignUpForm
    template_name = 'dashboard/register.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        user = form.save(commit=False)
        # print(user)
        messages.success(self.request, 'Successfully registered')
        user.save()
        return super().form_valid(form)
 
class Logout(LogoutView):
    pass

class ProfileView(TemplateView):
    template_name = 'dashboard/profile-view.html'

def home(request):
    return render(request,'dashboard/home.html',{})

