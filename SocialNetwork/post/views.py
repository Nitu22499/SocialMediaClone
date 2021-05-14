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

# Imports for ml algorithm 
from keras.preprocessing import image
from keras.models import load_model
import numpy as np
import cv2
import imutils
import datetime
import pickle as pkl
from sklearn.externals import joblib
# endml

def predict_illegal_image_post(post):
    gun_cascade = cv2.CascadeClassifier('gun_detector.xml')
    # camera = cv2.VideoCapture('data/gun4_2.mp4')
    image = cv2.imread(post)
    gun_exist = False
    image = imutils.resize(image, width=500)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))

    if len(gun) > 0:
        gun_exist = True
        
    print("{} gun detected...".format(len(gun)))


    for (x, y, w, h) in gun:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # show the output image------ isko off hi rhne dena
    # cv2.imshow("Image", image)
    cv2.waitKey(0)

    if gun_exist:
        print("guns detected")
        prediction = "guns detected"
    else:
        print("guns NOT detected")
        prediction = "guns NOT detected"
    
    return prediction

def predict_illegal_video_post(post):
    gun_cascade = cv2.CascadeClassifier('gun_detector.xml')
    camera = cv2.VideoCapture(post)


    # camera = cv2.VideoCapture(0)

    # initialize the first frame in the video stream
    firstFrame = None

    # loop over the frames of the video

    gun_exist = False

    while True:
        (grabbed, frame) = camera.read()

        # if the frame could not be grabbed, then we have reached the end of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
        
        if len(gun) > 0:
            gun_exist = True
            
        for (x,y,w,h) in gun:
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]    

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # draw the text and timestamp on the frame
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    #     below line is to show gun detection window to isko off hi rkhna
    #     cv2.imshow("Security Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if gun_exist:
        print("guns detected")
        prediction = "guns detected"
    else:
        print("guns NOT detected")
        prediction = "guns NOT detected"
    
    return prediction

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
        print(self.object, self.object.post_image.url[-4:])
        print(self.object.post_image.path)
        if self.object.post_image.url[-4:] == ".mp4":
        #     illegal_post_result = predict_illegal_video_post(self.object.post_image.path)
            return super(HomeView, self).form_valid(form)
        illegal_post_result = predict_illegal_image_post(self.object.post_image.path)
        res = predict_node_or_safe(self.object.post_image.path)

        if res == 'normal image' and illegal_post_result == 'guns NOT detected':
            # print(self.object)
            messages.success(self.request, 'File uploaded!')
            return super(HomeView, self).form_valid(form)
        elif illegal_post_result == 'guns detected': 
            messages.warning(self.request, 'Warning: You have illegal post. Please maintain Decorum. Otherwise user will be blocked')
            return super(HomeView, self).form_valid(form)
        elif res == 'nude image':
            # print(self.object)
            self.object.delete()
            # print(self.object)
            p = User.objects.get(id=self.request.user.id)
            if p.nude_count < 3 :
                messages.warning(self.request, 'Warning: You have used abusive post. Please maintain Decorum. Otherwise user will be blocked')
            
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
