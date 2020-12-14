from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView, RedirectView,TemplateView,DeleteView
from django.contrib import messages
from .models import *
from dashboard.models import User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.http import Http404
# Create your views here.
# ml
# import numpy as np
# import pandas 
from sklearn.externals import joblib
# endml




# def _get_profane_prob(prob):
#     return prob[1]

# def preprocess(text):
#     list_text = list(text.split())
#     print(list_text)
#     for word in list_text:
#         predict(word)
#     return

def predict(text):
#     list_text = list(text.split())
# #     print(list_text)
#     for text in list_text:
# #         predict(word)
    vectorizer = joblib.load('vectorizer.joblib')
    model = joblib.load('model.joblib')

    result = model.predict(vectorizer.transform(text))
    if result == 1:
        print('it contains vulgar words', text )
        return result
    else:
        print('It is normal message', text)
        return result
        
            
# def predict_prob(texts):
#     return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))



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
    counter=0
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        print(comment.content)

        val=predict([comment.content])
        print(val[0])
        if val==1:
            messages.warning(request, 'Warning: You have used abusive word. Please maintain Decorum. Otherwise user will be blocked')
            counter=counter+1
            print(counter)
        return redirect(reverse_lazy('post:home'))
    else:
        return redirect(reverse_lazy('post:home'))

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # template_name = 'dashboard/home.html'
    success_url = reverse_lazy('post:home')

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     print(pk)
    #     obj = Post.objects.get(pk=pk)
    #     print(obj)
    #     if not obj.user == self.request.user:
    #         messages.warning(self.request, 'You need to be the author of the post in order to delete it')
    #     return obj.delete()


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    # template_name = 'dashboard/home.html'
    success_url = reverse_lazy('post:home')

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     print(pk)
    #     Comment.objects.filter(id=pk).delete()
        
