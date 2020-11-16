from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, RedirectView,TemplateView,DeleteView
from django.contrib import messages
from .models import *
from dashboard.models import User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
        posts = Post.objects.all().order_by('-post_date')
        print(posts)
        kwargs['posts'] = posts
        print(kwargs['posts'])
        return super().get_context_data(**kwargs)

@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        user = User.objects.get(username=user)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value=='Like':
                like.value='Unlike'
            else:
                like.value='Like'
        else:
            like.value='Like'

            post_obj.save()
            like.save()

    return redirect('post:home')

def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        return redirect(reverse_lazy('post:home'))
    else:
        return redirect(reverse_lazy('post:home'))

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'dashboard/home.html'
    success_url = reverse_lazy('post:home')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        print(pk)
        obj = Post.objects.get(pk=pk)
        print(obj)
        if not obj.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj.delete()