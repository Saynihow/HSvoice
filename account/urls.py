from django.conf.urls import url
from . import views
default_encoding = 'utf-8'
urlpatterns = [
    #url(r'^login/$', views.user_login, name='login')
    url(r'^login/$', 'django.contrib.auth.views.login', name='login',),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^register/$', views.register, name='register'),
    url(r'^upload_image/$', views.model_form_upload_image, name='upload_image'),
    url(r'^upload_voice/$', views.model_form_upload_voice, name='upload_voice'),
    url(r'^profile/$', views.profile_data, name='profile'),
    url(r'^profile/edit_img/(?P<id>\d+)/$', views.edit_profile_image, name=''),
    url(r'^profile/edit_voice/(?P<id>\d+)/$', views.edit_profile_voice_list, name=''),
    url(r'^profile/edit_voice/(\d+)/edit_voice_detail/(?P<id>\d+)/$', views.edit_profile_voice_detail, name='edit_voice_detail'),
    url(r'^profile/delete_img/(?P<id>\d+)/$', views.image_delete, name='image_delete'),
]