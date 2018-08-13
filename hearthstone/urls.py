from django.conf.urls import url
from . import views
default_encoding = 'utf-8'
#app_name = 'hearthstone'
urlpatterns = [
    url(r'^$', views.index, name='HS'),
    url(r'^search/$', views.image_search, name='image_search'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
        r'(?P<title>[-\w]+)/$',
        views.index_detail,
        name='index_detail'),
]