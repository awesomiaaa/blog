# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ReplyPost, Chat, Post, UserProfileInfo, Event, Comment, Liker,Aboutview,Work,Message
# Register your models here.


admin.site.register(Post)
admin.site.register(UserProfileInfo)
admin.site.register(Event)
admin.site.register(Chat)
admin.site.register(ReplyPost)
admin.site.register(Comment)
admin.site.register(Liker)
admin.site.register(Aboutview)
admin.site.register(Work)
admin.site.register(Message)