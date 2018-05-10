from django import forms
from django.contrib.auth.models import User
from .models import ReplyPost, Post, UserProfileInfo, Event, Comment, Liker,Aboutview,Work,Message


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','email','username','password')
        labels = {
            'email': 'Email Address'
        }



class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',)
        labels = {
            'profile_pic': 'Choose Picture'
        }


class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=['title','text']

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = [ 'eventname','description', 'eventdate', 'eventstart', 'eventend','event_pic',]
        labels = {
            'eventname': 'Event Name',
            'eventdate': 'Event Date',
            'eventstart': 'Event Start',
            'eventend': 'Event End',
        }
        widgets = {
            'eventdate': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': "eventdate"}),
            'eventstart': forms.TimeInput(attrs={'placeholder': 'HH:MM','id':"eventstart"}),
            'eventend': forms.TimeInput(attrs={'placeholder': 'HH:MM','id':"eventend"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields=['body']

class LikerForm(forms.ModelForm):
    class Meta:
        model= Liker
        fields=['like']

class AboutviewForm(forms.ModelForm):
    class Meta:
        model= Aboutview
        fields=['bio','talents','telephone','workdetail']


class WorkForm(forms.ModelForm):
    class Meta:
        model= Work
        fields=['work_pic','description']
class MessageForm(forms.ModelForm):
    class Meta:
        model= Message
        fields=['msg']
