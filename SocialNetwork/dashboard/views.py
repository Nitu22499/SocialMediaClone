from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView,TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import *
from .forms import UserSignUpForm, EditProfileForm, UploadProfilePicForm
from post.models import *
from django.forms.models import model_to_dict
from post.views import *

# Create your views here.

class Login(LoginView):
    template_name = 'dashboard/login.html'
    

class RegisterView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'dashboard/register.html'

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        user = form.save(commit=False)
        # print(user)
        messages.success(self.request, 'Successfully registered')
        user.save()
        login(self.request, user)
        return redirect('post:home')

        return kwargs


 
class Logout(LogoutView):
    pass

class ProfileView(CreateView):
    template_name = 'dashboard/profile-view.html'
    model=Post
    def get_context_data(self, **kwargs):
        user=self.request.user
        posts=Post.objects.filter(user=user)
        kwargs['posts']=posts
        return kwargs

class Edit_Profile(FormView):
    model = User
    form_class = EditProfileForm
    template_name = 'dashboard/edit_profile.html'
    success_url = reverse_lazy('dashboard:profile')
    
    def get_object(self):
        """Check if data already exists"""
        try:
            self.object = User.objects.get(username= self.request.user)
            print(self.object)
            return self.object
        except:
            return None

    def get_initial(self):
        """Pre-fill the form if data exists"""
        obj = self.get_object()
        print(obj)
        if obj is not None:
            initial_data = model_to_dict(obj)
            print(initial_data)
            initial_data.update(model_to_dict(obj))
            print(initial_data)
            return initial_data
        else:
            return super().get_initial()

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        print(self.object)
        User.objects.filter(username=self.object).update(
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            email = form.cleaned_data['email'],
            gender = form.cleaned_data['gender'],
            date_of_birth = form.cleaned_data['date_of_birth'],
        )
        messages.success(self.request, 'Edited successfully')
        return super().form_valid(form)


    
def searchUser(request):
    
    if request.method == 'GET': # this will be GET now      
        searchfriend =  request.GET.get('searchfriend') # do some research what it does       
        user = User.objects.filter(username=searchfriend)
        print(user)
        return render(request,'dashboard/profile-view.html',{'user':user})

class UploadProfilePic(FormView):
    model = User
    form_class = UploadProfilePicForm
    template_name = 'dashboard/upload-profile.html'
    success_url = reverse_lazy('dashboard:profile')

    def get_object(self):
        """Check if data already exists"""
        try:
            self.object = User.objects.get(username= self.request.user)
            print(self.object)
            return self.object
        except:
            return None

    def get_initial(self):
        """Pre-fill the form if data exists"""
        obj = self.get_object()
        print(obj)
        if obj is not None:
            initial_data = model_to_dict(obj)
            print(initial_data)
            initial_data.update(model_to_dict(obj))
            print(initial_data)
            return initial_data
        else:
            return super().get_initial()

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        User.objects.filter(username=self.object).update(
            user_image =form.cleaned_data['user_image'],
        )
        messages.success(self.request, 'Image uploaded successfully')
        return super().form_valid(form)

    