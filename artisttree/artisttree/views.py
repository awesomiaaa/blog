# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse,HttpResponseRedirect,HttpResponse
from django.shortcuts import render, get_object_or_404
from .forms import  UserForm, CommentForm, PostForm, UserProfileInfoForm, EventForm, LikerForm,AboutviewForm,WorkForm,MessageForm
from .models import User, ReplyPost, Chat, Post, UserProfileInfo, Event, Comment,Liker,Aboutview,Work
from django.utils import timezone
from django.db.models import Q

from django.conf import settings as conf_settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail
import requests
# Create your views here.
def front(request):
    return render(request, 'artisttree/front.html', context=None)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                u = User.objects.get(username=username)
                request.session['user_id'] = u.id
                request.session['user_username'] = u.username

                return HttpResponseRedirect('/artisttree/all',{'post': Post.objects.all()})

            else:
                return render(request, 'artisttree/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'artisttree/login.html', {'error_message': 'Invalid login'})
    return render(request, 'artisttree/login.html')


def register(request):
    user_form = UserForm(data=request.POST)
    profile_form = UserProfileInfoForm(request.POST or None ,request.FILES or None)

    if user_form.is_valid() and profile_form.is_valid():
        user = user_form.save()
        user.set_password(user.password)
        user.save()
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()

        return HttpResponseRedirect('/artisttree/login_user')
    else:
            # One of the forms was invalid if this else gets called.
        print(user_form.errors,profile_form.errors)
    context ={
        'form': user_form,
        'form2': profile_form,
    }
    return render(request, 'artisttree/register.html',  context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'artisttree/login.html', context)


def create_post(request):
        form=PostForm(data=request.POST)

    #    posts = User.objects.filter(id=request.session['user_id'])
        if form.is_valid():
            save_it = form.save(commit = False)
            save_it.user = request.user
            save_it.save()
            context={'form':form}
            form.save()

            return HttpResponseRedirect('/artisttree/all',context)
        else:
            form=PostForm()
            context={'form':form}
        return render(request,'artisttree/create_post.html',context)
def create_bio(request):
    form = AboutviewForm(data=request.POST)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.user = request.user
        save_it.save()
        context = {'form': form}
        form.save()

        return HttpResponseRedirect('/artisttree/all', context)
    else:
        form = AboutviewForm()
        context = {'form': form}
    return render(request, 'artisttree/create_bio.html', context)
def post(request):
    comment = Comment.objects.all()
    post = Post.objects.all().order_by('-date_posted', '-time_posted')
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    print (comment)
    return render(request,'artisttree/post.html',{'post': post, 'userprofilepic':userprofileinfo,'comment':comment})

def uploadpic(request):

    form =WorkForm(data=request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = user
        if 'profile_pic' in request.FILES:
            print('found it')
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        context={'form':form}
        print ('lkkk')
        return HttpResponseRedirect('/artisttree/all', context)
    else:
        form = WorkForm()
        context = {'form': form}
    return render(request, 'artisttree/create_workpic.html', context)
def postdetail(request, postdetail_id=1):
    comment=Comment.objects.all()
    post = Post.objects.get(id=postdetail_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request, 'artisttree/post_detail.html',{'userprofilepic':userprofileinfo, 'post':post,'comment':comment,'like':like})

def update_post(request,postdetail_id=None):
    instance = get_object_or_404(Post,id=postdetail_id)
    form = PostForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/artisttree/all')
    context = {
        'form': form,
        'instance':instance,
    }

    return render(request, 'artisttree/create_post.html', context)

def update_event(request,postdetail_id=None):
    instance = get_object_or_404(Event,id=postdetail_id)
    form = EventForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/artisttree/all')
    context = {
        'form': form,
        'instance':instance,
    }

    return render(request, 'artisttree/create_post.html', context)
def delete_post(request, postdetail_id):
    postdetail = Post.objects.get(pk=postdetail_id)
    postdetail.delete()
   ## article = Article.objects.filter(user=request.user)
    return HttpResponseRedirect('/artisttree/all')

def delete_event(request, eventsingle_id):
    event = Event.objects.get(pk=eventsingle_id)
    event.delete()
   ## article = Article.objects.filter(user=request.user)
    return HttpResponseRedirect('/artisttree/all')



def like(request,postdetail_id):

    if postdetail_id:
         a = Post.objects.get(id=postdetail_id)
         count = a.likes
         if count==False:
            count+=1
            a.likes = count
            a.save()
         else:
             count-=1
             a.likes = count
             a.save()

    return render(request,'artisttree/post_detail.html',{'post':Post.objects.get(id=postdetail_id)})

def liker(request,postdetail_id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=postdetail_id)
    try:
        check=LikerForm.objects.get(user=user,post=post)
    except Liker.DoesNotExist:
        check=None
    if check is None:
        x=Liker.objects.get(user=user, post=post, like=like)
        x.save()
        if like == 'like':
            post.likes=post.likes+1
        elif like == 'unlike':
            post.likes=post.likes-1
            post.save()

    return HttpResponseRedirect('/artisttree/all')


def create_comment(request,postdetail_id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id = postdetail_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = user
        instance.post = post
        instance.save()
        print('kkkkkk')
        return HttpResponseRedirect('/artisttree/all')
    else:
        form = CommentForm()
        context = {
            'form': form,

        }
        return render(request, 'artisttree/create_comment.html', context)


def comments(request):
    post = ReplyPost.objects.all()
    context= {
        'comment':post
    }
    return render(request,'artisttree/get/{{postdetail.id}}',context)


def profile(request):
    post = Post.objects.filter(user=request.session['user_id']).order_by('-date_posted', '-time_posted')
    userinfo = User.objects.get(id=request.session['user_id'])
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request,"artisttree/profile.html",{'post':post, 'user':userinfo,'userprofilepic':userprofileinfo,})

def profileQQ(request,profile_id):
##### profile mo
    user=User.objects.get(id=profile_id)
    post = Post.objects.filter(user_id=profile_id).order_by('-date_posted', '-time_posted')
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    print (post)
    context = {'user':user,
               'post':post,
                 'userprofilepic':userprofileinfo
               }
    return render(request,"artisttree/789.html",context)


def profilepostdetail(request, postdetail_id=1):

    ##porfile post mo
    comment = Comment.objects.all()
    post = Post.objects.get(id=postdetail_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    return render(request, 'artisttree/profile_post.html',
                  {'userprofilepic': userprofileinfo, 'post': post, 'comment': comment})

def profilepostdetail1(request, postdetail_id=1,profile_id=1):

    ##porfile post mo
    comment = Comment.objects.all()
    post = Post.objects.get(id=postdetail_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    return render(request, 'artisttree/post_detail.html',
                  {'userprofilepic': userprofileinfo, 'post': post, 'comment': comment})



def editprofile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST, instance=request.user)
        profile_form = UserProfileInfoForm(request.POST or None, request.FILES or None, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

        #profile.user = user
        #profile.save()
            if 'profile_pic' in request.FILES:
                update_pic = UserProfileInfo.objects.get(user_id=request.session['user_id'])
                update_pic.profile_pic = request.FILES['profile_pic']
                update_pic.save()
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        u = User.objects.get(username=username)
                        request.session['user_id'] = u.id
                        request.session['user_username'] = u.username
        return HttpResponseRedirect('/artisttree/profile')
    else:
        form = UserForm(instance=request.user)
        profile_form = UserProfileInfoForm(instance=request.user)

        context = {
            'form': form,
            'form2': profile_form
        }
    return render(request,'artisttree/editprofile.html',context)


def about(request):
   # post = Post.objects.filter(user=request.session['user_id'])
    userinfo = User.objects.get(id=request.session['user_id'])
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    bio = Aboutview.objects.get(user_id=request.session['user_id'])
    #bio = Aboutview.objects.filter(user_id=request.session['user_id'])

    return render(request,"artisttree/about.html",{'user':userinfo,'userprofilepic':userprofileinfo,'bio':bio,'userprofileinfo':userprofileinfo})

def update_bio(request):
    instance = Aboutview.objects.get(user_id=request.session['user_id'])
    form = AboutviewForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect('/artisttree/all')

    context = {'form': form,
               'instance':instance,
              }
    return render(request, "artisttree/create_bio.html", context)


def aboutview(request,profile_id):
    userinfo = User.objects.get(id=profile_id)
    bio = Aboutview.objects.get(user_id=profile_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request, "artisttree/aboutview.html", {'user': userinfo, 'userprofilepic': userprofileinfo,'bio':bio})


def contact(request):
    userinfo = User.objects.get(id=request.session['user_id'])
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
    bio = Aboutview.objects.get(user_id=request.session['user_id'])
    # msg = "ARTISTTREE TEXTING \nReceiver: {} {}! \nSender: {}\nThank You\n".format(userinfo.first_name, userinfo.last_name, profile)
    #
    # url = 'https://www.isms.com.my/isms_send.php?un=%s&pwd=%s&dstno=%d&msg=%s&type=1&sendid=GardenMirrorEventsPlace' % ("royce236", "261523", 639367343513, msg)
    # txt = requests.get(url)  # proxies={"https":"http://proxy.server:3128"})

    return render(request,"artisttree/contact.html",{'user':userinfo,'userprofilepic':userprofileinfo,'bio':bio})

def contactview(request,profile_id):

    userinfo = User.objects.get(id=profile_id)
    bio = Aboutview.objects.get(user_id=profile_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])


    msg = "ARTISTTREE TEXTING \nReceiver: {} {}! \nSender: {}  \nMessage you: {} \nThank You!".format(userinfo.first_name, userinfo.last_name, userprofileinfo.user.first_name,userprofileinfo.user.last_name)
    url = 'https://www.isms.com.my/isms_send.php?un=%s&pwd=%s&dstno=%d&msg=%s&type=1&sendid=GardenMirrorEventsPlace' % ("royce236", "261523", bio.telephone, msg)
    txt = requests.get(url)  # proxies={"https":"http://proxy.server:3128"})

    return render(request, "artisttree/contactview.html",{'user': userinfo, 'userprofilepic': userprofileinfo, 'bio': bio})


def work(request):
    userinfo = User.objects.get(id=request.session['user_id'])
    bio = Aboutview.objects.get(user_id=request.session['user_id'])
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request,"artisttree/work.html",{'user':userinfo,'userprofilepic':userprofileinfo,'bio':bio})

def workview(request,profile_id):
    userinfo = User.objects.get(id=profile_id)
    bio = Aboutview.objects.get(user_id=profile_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request,"artisttree/workview.html",{'user':userinfo,'userprofilepic':userprofileinfo,'bio':bio})


def single(request):
    return render(request, 'artisttree/single.html')



def event(request):
    user = User.objects.get(id=request.session['user_id'])
    event = Event.objects.all().order_by('-date_posted', '-time_posted')
    #event = Event.objects.filter(user=request.session['user_id']).order_by('-date_posted', '-time_posted')
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request, 'artisttree/event.html', {'event': event, 'userprofilepic':userprofileinfo,'user':user})

def event1(request):
    user = User.objects.get(id=request.session['user_id'])
   # event = Event.objects.all().order_by('-date_posted', '-time_posted')
    event = Event.objects.filter(user=request.session['user_id']).order_by('-date_posted', '-time_posted')
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

    return render(request, 'artisttree/eventprofile.html', {'event': event, 'userprofilepic':userprofileinfo,'user':user})


def eventsingle(request, eventsingle_id):
    event = Event.objects.get(id=eventsingle_id)
    userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])

   # print(event.user.userprofileinfo.profile_pic)

    return render(request, 'artisttree/event_single.html', {'userprofileinfo':userprofileinfo, 'event':event})

def create_event(request):
    if not request.user.is_authenticated():
        return render(request, 'artisttree/login.html')
    else:
        form = EventForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()

            return HttpResponseRedirect('/artisttree/event')
        context = {
            "form": form,
        }
        return render(request, 'artisttree/create_event.html', context)
















        # print('Hello')
        # form = EventForm(request.POST,request.FILES)
        # if form.is_valid():
        #     save_it = form.save(commit=False)
        #     save_it.user = request.user
        #     # save_it.save()
        #     if 'event_pic' in request.FILES:
        #         print('Found it')
                # current_user = request.user
                # update_pic = Event.objects.get(user_id=request.session['user_id'])
                # update_pic.event_pic = request.FILES['event_pic']
                # update_pic.save()

        # if 'event_pic' in request.FILES:
        #     print('found it')
        #     save_it=Event.objects.get(user_id=request.session['user_id'])
        #     save_it.event_pic = request.FILES['event_pic']
        #     save_it.save()
#             return HttpResponseRedirect('/artisttree/event')
#         else:
#             form = EventForm()
#             context = {'form': form}
#             return render(request, 'artisttree/create_event.html', context)
# #
#
# def create_event1(request):
#     user = User.objects.get(id=request.session['user_id'])
#     userprofileinfo = UserProfileInfo.objects.get(user_id=request.session['user_id'])
#     form=EventForm(user=request.POST or None)
#     if form.is_valid():
#         save_it = form.save(commit = False)
#         save_it.event_pic=request.user
#         save_it.user = request.user
#         save_it.save()
#
#         if 'event_pic' in request.FILES:
#             print('found it')
#             event.event_pic = request.FILES['event_pic']
#             event.save()
#         return HttpResponseRedirect('/artisttree/eventview',context)
#     else:
#         form=EventForm()
#         context={'form':form}
#         return render(request,'artisttree/create_event.html',context)
#

def search_titles(request):
    spost = Post.objects.all().order_by('-date_posted', '-time_posted')
    query = request.GET.get("q")
    if query:
        post = spost.filter(
            Q(title__icontains=query)
        ).distinct()
        context = {'post': post,

                   }

        return render(request, 'artisttree/search.html', context)
    else:
        context = {'post': all}
        return render(request, 'artisttree/search.html', context)


def search_events(request):
    sevent = Event.objects.all().order_by('-time_posted')
    query = request.GET.get("q")
    if query:
        event1 = sevent.filter(
            Q(eventname__icontains=query)
        ).distinct()
        context = {'event': event1,

                   }

        return render(request, 'artisttree/searchevents.html', context)
    else:
        context = {'event': all}
        return render(request, 'artisttree/searchevents.html', context)


def Home(request):
    c = Chat.objects.all()

    return render(request, "artisttree/home.html", {'home': 'active', 'chat': c})

def Postchat(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        if msg != '':
            c.save()

        return JsonResponse({ 'msg': msg, 'user': c.user.username })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    user = User.objects.get(id=request.session['user_id'])
    c = Chat.objects.all()

   # c=Chat.objects.get(id=user.id)

    return render(request, 'artisttree/messages.html', {'chat': c,'user':user})


def SampleEvent(request):
    form=SampleEventForm(request.POST or None ,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        print (instance)
        messages.success(request,"SUCCESS")
        return HttpResponseRedirect('/artisttree/sampleevent')
    context={
        'form':form,
    }
    return render(request, 'artisttree/create_event.html', context)





