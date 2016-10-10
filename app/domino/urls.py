from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sshlogon(?P<server_id>[0-9]+)', views.sshlogon, name='sshlogon'),
    #url(r'^(?P<server_id>[0-9]+)/', views.index, name='index'),
]

