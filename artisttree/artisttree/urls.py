from django.conf.urls import url
from . import views

app_name = 'artisttree'

urlpatterns = [
    
    url(r'^$', views.front, name='front'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    

    url(r'^all/', views.post, name='all'),
    #url(r'^get/(?P<postdetail_id>[0-9]+)/$', views.postdetail, name='get'),
    url(r'^create_post/', views.create_post,name='create_post'),
   # url(r'^post/(?P<user>.*)/(?P<title>.*)', views.postdetail, name='postdetail'),
   # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<postdetail_id>[0-9]+)/$', views.postdetail, name='post'),
    url(r'^post/(?P<postdetail_id>[0-9]+)/edit/$', views.update_post, name='update_post'),
    url(r'^post/(?P<postdetail_id>[0-9]+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<postdetail_id>[0-9]+)/like/$',views.like, name='like'),
    url(r'^post/(?P<postdetail_id>[0-9]+)/comment/$', views.create_comment, name='create_comment'),


    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profileQQ, name='profileQQ'),
    url(r'^profile/(?P<profile_id>[0-9]+)/post/(?P<postdetail_id>[0-9]+)/$', views.profilepostdetail1, name='profilepostdetail1'),
    url(r'^profile/(?P<profile_id>[0-9]+)/about/$', views.aboutview, name='aboutview'),
    url(r'^profile/(?P<profile_id>[0-9]+)/work/$', views.workview, name='contactview'),
    url(r'^profile/(?P<profile_id>[0-9]+)/contact/$', views.contactview, name='contactview'),
    url(r'^profile/(?P<profile_id>[0-9]+)/contact/msg$', views.contactview, name='contactview'),
    url(r'^create_bio/$', views.create_bio,name='create_bio'),
    url(r'^update_bio/$', views.update_bio,name='update_bio'),

    #url(r'^profile/(?P<profile_id>[0-9]+)/contact/$', views.aboutview, name='aboutview'),
    url(r'^profile/edit/$', views.editprofile, name='editprofile'),
    url(r'^profile/(?P<postdetail_id>[0-9]+)/post/$', views.profilepostdetail, name='profilepostdetail'),
    #url(r'^profile/(?P<postdetail_id>[0-9]+)/post1/$', views.profilepostdetail1, name='profilepostdetail1'),

    url(r'^profile/(?P<postdetail_id>[0-9]+)/post1/$', views.update_post, name='update_post'),
    
    url(r'^about/$', views.about, name='about'),
    url(r'^work/$', views.work, name='work'),
    url(r'^work/uploadpic/$', views.uploadpic, name='uploadpic'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^single/$', views.single, name='single'),

    url(r'^event/$', views.event, name='event'),
    url(r'^profile/event$', views.event1, name='event1'),
    url(r'^event/(?P<eventsingle_id>[0-9]+)/$', views.eventsingle, name='eventsingle'),
    url(r'^event/(?P<eventsingle_id>[0-9]+)/delete/$', views.delete_event, name='delete_event'),
    url(r'^event/(?P<eventsingle_id>[0-9]+)/edit/$', views.update_event, name='update_event'),

    url(r'^create_event/$', views.create_event,name='create_event'),
    # url(r'^create_eventt/$', views.create_event1 ,name='create_event1'),
   # url(r'^eventsingle/', views.eventsingle, name='eventsingle'),

#    url(r'^retrieveEvent/', views.retrieveEvent, name='retrieveEvent'),
#    url(r'^makeevent/', views.makeevent, name='makeevent'),
    
 #   url(r'^create/$', views.post_create),
    #url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'),
 #   url(r'^(?P<slug>[\w-]+)/all$', views.PostDetailView.as_view(), name='detail'), #Django Code Review #3 on joincfe.com/youtube/
 #   url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
 #   url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

    url(r'^search/$', views.search_titles,name='search'),
    url(r'^searchevents/$', views.search_events,name='searchevents'),

    url(r'^home/$', views.Home, name='home'),

    url(r'^post/$', views.Postchat, name='post'),
    url(r'^messages/$', views.Messages, name='messages'),
]


