from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, RedirectView,TemplateView
from django.contrib import messages
from .models import Post
from .forms import PostForm

# Create your views here.

class HomeView(CreateView):
    model = Post
    template_name = 'dashboard/home.html'
    form_class = PostForm
    success_url = reverse_lazy('post:home')

    def form_valid(self, form):
        print(form)
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.success(self.request, 'File uploaded!')
        return super(HomeView, self).form_valid(form)
                
    def get_context_data(self, **kwargs):
        posts = Post.objects.all()
        kwargs['posts'] = posts
        print(kwargs['posts'])
        return super().get_context_data(**kwargs)


def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        return redirect(reverse_lazy('post:home'))
    else:
        return redirect(reverse_lazy('post:home'))
