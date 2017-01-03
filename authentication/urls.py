from django.conf.urls import include, url
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
    url(r'^changeuserinfo/$', authentication.views.change_user_info),
    url(r'^changecompanyinfo/$', authentication.views.change_company_info),
    ]