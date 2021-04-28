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
from django.http import Http404, HttpResponseRedirect
import os
from keras.preprocessing import image
from keras.models import load_model
import numpy as np

# Create your views here.
# ml
# import numpy as np
# import pandas 
from sklearn.externals import joblib
# endml

def predict_node_or_safe(post_image):
    model = load_model('model_saved.h5')
    # print(model.summary())
    test_image = image.load_img(post_image, target_size = (224,224))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    # print(result)
    # training_set.class_indices
    if(result[0][0] == 1):
        prediction = 'nude image'
    else:
        prediction = 'normal image'
        
    # print(prediction)
    return prediction


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
        # print('it contains vulgar words', text )
        return result
    else:
        # print('It is normal message', text)
        return result
        
            
# def predict_prob(texts):
#     return np.apply_along_axis(_get_profane_prob, 1, model.predict_proba(vectorizer.transform(texts)))



class HomeView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'dashboard/home.html'
    form_class = PostForm
    success_url = reverse_lazy('post:home')

    def form_valid(self, form): 
             
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        # print(self.object.post_image.path)

        res = predict_node_or_safe(self.object.post_image.path)

        if res == 'normal image':
            # print(self.object)
            
            messages.success(self.request, 'File uploaded!')
            return super(HomeView, self).form_valid(form)
        elif res == 'nude image': 
            # print(self.object)
            self.object.delete()
            # print(self.object)
            p = User.objects.get(id=self.request.user.id)
            if p.nude_count < 3 :
                messages.warning(self.request, 'Warning: You have used abusive word. Please maintain Decorum. Otherwise user will be blocked')
            
                print(p.nude_count)
                p.nude_count = p.nude_count + 1
                print(p.nude_count)
                p.save()
            # print(counter)
            if p.nude_count >= 3 :
            
                print(p.is_active)
                p.is_active = False
                p.save()
                print(p.is_active)
                
                messages.warning(self.request, 'You account is suspended!! You have used abusive post despite the warning ')
                return render(self.request, "dashboard/block.html", {})
        
            return HttpResponseRedirect(self.get_success_url())
                
    def get_context_data(self, **kwargs):
        posts = Post.objects.all().order_by('-post_date')
        # print(posts)
        kwargs['posts'] = posts
        # print(kwargs['posts'])
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

@login_required
def create_comment(request, post_id=None):
    
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        print(comment.id)

        val=predict([comment.content])
        # print(val[0])
        p = User.objects.get(id=request.user.id)
        if val==1:
            if p.bad_word_count < 3 :
                messages.warning(request, 'Warning: You have used abusive word. Please maintain Decorum. Otherwise user will be blocked')
            
                print(p.bad_word_count)
                p.bad_word_count = p.bad_word_count + 1
                print(p.bad_word_count)
                p.save()
            # print(counter)
        if p.bad_word_count >= 3 :
           
            print(p.is_active)
            p.is_active = False
            p.save()
            print(p.is_active)
            
            messages.warning(request, 'You account is suspended!! You have used abusive word despite the warning ')
            return render(request, "dashboard/block.html", {})
        
        return redirect(reverse_lazy('post:home'))
    else:
        return redirect(reverse_lazy('post:home'))

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:home')

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('post:home')
