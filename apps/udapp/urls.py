from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^edit$', views.edit),
    url(r'^edit/(?P<uid>\d+)$', views.edit),
    url(r'^edit/description/(?P<uid>\d+)$', views.edit_description),
    url(r'^edit/password/(?P<uid>\d+)$', views.edit_password),
    url(r'^message/(?P<rid>\d+)/(?P<aid>\d+)$', views.create_message),
    url(r'^new$', views.create),
    url(r'^remove/(?P<uid>\d+)$', views.remove),
    url(r'^reply/(?P<mid>\d+)/(?P<aid>\d+)$', views.create_reply),
    url(r'^show/(?P<uid>\d+)$', views.show),
]