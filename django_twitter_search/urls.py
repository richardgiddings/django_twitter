from django.conf.urls import url
from . import views

app_name = 'django_twitter_search'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/$', views.search, name="search"),
    url(r'^save/$', views.save, name='save'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^delete/(?P<tweet_id>\d+)/$', views.delete, name='delete'),
]
