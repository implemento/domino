from django.conf.urls import url
from .views import OpenTerminalRedirectView
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sshlogon/(?P<server_id>[0-9]+)',
        OpenTerminalRedirectView.as_view(url='http://localhost:3000/'),
        name='terminal'),
]
