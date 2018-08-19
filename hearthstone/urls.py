from django.conf.urls import url
from . import views
default_encoding = 'utf-8'
#app_name = 'hearthstone'
urlpatterns = [
    url(r'^$', views.index, name='HS'),
    url(r'^search/$', views.image_search, name='image_search'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<author_id>\d+)/' \
        r'(?P<id>\d+)/$',
        views.index_detail,
        name='index_detail'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.index,
        name='image_list_by_tag'),
    url(r'^like_image/$', views.image_like, name='like_image'),
]