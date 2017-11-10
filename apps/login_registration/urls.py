from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout), # clear session
    # dashboard
    url(r'^dashboard$', views.dashboard),
    url(r'^dashboard/admin$', views.dashboard_admin),
    # extra functions
    url(r'^reset$', views.reset), # clear DB
]