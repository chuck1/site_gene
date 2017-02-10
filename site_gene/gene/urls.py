
from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<person_pk>[0-9]+)/ancestors/$', views.ancestors, name='ancestors'),
        url(r'^(?P<person_pk>[0-9]+)/descendents/$', views.descendents, name='descendents'),
        ]
