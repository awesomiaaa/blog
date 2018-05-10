# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User
from django.utils import timezone


#class User(models.Model):
#    username = models.CharField(max_length=50)
#    password = models.CharField

class Post(models.Model):
    user = models.ForeignKey(User,related_name='user', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    likes = models.IntegerField(default=False)
    date_posted = models.DateField(auto_now=True)
    time_posted = models.TimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    def __str__(self):
        return self.text

class Aboutview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio=models.TextField()
    workdetail= models.TextField()

    talents=models.TextField()
    telephone = models.IntegerField()
    def __str__(self):
        return self.user.first_name

class Work(models.Model):
    user = models.OneToOneField(User)
    description=models.CharField(max_length=100)
    work_pic = models.ImageField(blank=True, upload_to='profile_pics')

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post=models.ForeignKey(Post,related_name='comments')
    user=models.ForeignKey(User)
    created=models.DateTimeField(auto_now_add=True)
    body=models.TextField()
    approved =models.BooleanField(default=False)

    def approved(self):
        self.approved=True
        self.save()

class Liker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.CharField(max_length=1000000000000000)

    def __int__(self):
        return self.user.id


class UserProfileInfo(models.Model):
    
    user = models.OneToOneField(User)

    # please pip install pillow before using 
    # Image field
    profile_pic = models.ImageField(blank=False,upload_to='profile_pics')

    def __str__(self):
        return self.user.username

class Message(models.Model):
    user = models.OneToOneField(User)
    msg=models.CharField(max_length=100)

    def __str__(self):
        return self.msg
class Event(models.Model):
    user = models.ForeignKey(User)
    eventname = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    eventdate = models.DateTimeField()
    eventstart = models.TimeField()
    eventend = models.TimeField()
    date_posted = models.DateField(auto_now=True)
    time_posted = models.TimeField(auto_now=True)
    event_pic =models.ImageField(blank=True,upload_to='event_pics')
    
    def __str__(self):
        eventname = "{} ({})".format(self.eventname, self.user)
        return self.eventname
    def __str__(self):
        return self.eventname



class Chat(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message

class ReplyPost(models.Model):
  #  post = models.ForeignKey(Article,on_delete=models.CASCADE)
  #  author = models.ForeignKey(Users,on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)
    date_posted = models.DateField(auto_now=True)
