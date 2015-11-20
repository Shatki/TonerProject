from django.conf.urls import patterns, include, url
from django.contrib import admin
import authentication.views


urlpatterns = [
    # Examples:
    # url(r'^$', 'toner.views.home', name='home'),
    url(r'^login/form/$', authentication.views.loadloginform),
    url(r'^register/form/$', authentication.views.loadregisterform),
    url(r'^login/$', authentication.views.login),
    url(r'^logout/$', authentication.views.logout),
    url(r'^register/$', authentication.views.register),
    ]