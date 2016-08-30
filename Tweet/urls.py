from django.conf.urls import url, include

from . import views,admin

urlpatterns = [
    url(r'^$', views.main, name='MainPage'),
    url(r'^main/$', views.main, name='MainPage'),
    url(r'^login/$', views.twitter_login),
    url(r'^logout/$', views.twitter_logout),
    url(r'^login/authenticated/$', views.twitter_authenticated),
    url(r'^home/$', views.home_page),
    url(r'^int/$', views.internal),
]
