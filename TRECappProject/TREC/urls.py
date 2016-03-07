from django.conf.urls import patterns, url
from TREC import views

urlpatterns = patterns('',
        url(r'^$', views.homepage, name='homepage'),
        )