from django.conf.urls import patterns, url

from tvb import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<obj_id>\d+)/$', views.clicked, name='clicked'),
)
