from django.shortcuts import render
from django.views.generic import CreateView, FormView, RedirectView,TemplateView
from .models import Post
from .forms import PostForm

# Create your views here.

class HomeView(FormView):
    model = Post
    template_name = 'dashboard/home.html'
    form_class = PostForm

    def form_valid(self,form):
        self.object = form.save(commit=False) 
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)