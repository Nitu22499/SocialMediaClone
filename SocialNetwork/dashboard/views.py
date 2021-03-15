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
from friend.models import FriendRequest
from django.forms.models import model_to_dict
from post.views import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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


 
class Logout(LoginRequiredMixin,LogoutView):
    pass

class ProfileView(LoginRequiredMixin,CreateView):
    template_name = 'dashboard/profile-view.html'
    model=Post
    def get_context_data(self, **kwargs):
        # print(self.kwargs['pk'])
        user=self.request.user
        kwargs['user']=user
        posts=Post.objects.filter(user=user)
        kwargs['posts']=posts
        friend_list_r = FriendRequest.objects.filter(receiver=user,status='friend')
        friend_list_s = FriendRequest.objects.filter(sender=user,status='friend')
        kwargs['friends']=friend_list_r|friend_list_s
        return kwargs
@login_required
def profile_view(request, pk):
    # print(request)
    user=User.objects.get(id=pk)
    posts=Post.objects.filter(user=user)
    friend_list_r = FriendRequest.objects.filter(receiver=user,status='friend')
    friend_list_s = FriendRequest.objects.filter(sender=user,status='friend')
    return render(request, 'dashboard/profile-view.html', {'user':user,'posts': posts,'friends':friend_list_r|friend_list_s})
    

class Edit_Profile(LoginRequiredMixin,FormView):
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

    
@login_required
def ajax_search(request):   
    if request.is_ajax():
        try:
            user = request.GET.get('user', None)
            user = User.objects.filter(username__icontains=user).values()
            html = render_to_string(
                template_name="dashboard/search.html", 
                context={"users": user}
            )

            data_dict = {"html_from_view": html}
            print(data_dict)
            return JsonResponse(data=data_dict, safe=False)
        except:
            return reverse_lazy('dashboard:search')

@login_required
def searchUser(request):
    
    if request.method == 'GET': # this will be GET now  
        searchfriend =request.GET.get('searchfriend') 
        print(searchfriend)  
        try:     
            user = User.objects.get(username=searchfriend)
            posts=Post.objects.filter(user=user)
            friend_list_r = FriendRequest.objects.filter(receiver=user,status='friend')
            friend_list_s = FriendRequest.objects.filter(sender=user,status='friend')
            return render(request, 'dashboard/profile-view.html', {'user':user,'posts': posts,'friends':friend_list_r|friend_list_s})
        except:
            return redirect(reverse_lazy('post:home'))

class UploadProfilePic(LoginRequiredMixin, FormView):
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
        myfile = self.request.FILES['user_image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        messages.success(self.request, 'Image uploaded successfully')
        return super().form_valid(form)

    