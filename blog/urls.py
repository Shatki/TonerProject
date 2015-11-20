from django.conf.urls import include, url
from django.contrib import admin
import authentication.views
import blog.views

urlpatterns = [
    # Examples:
    url(r'^article(?P<article_id>\d+)/addlike/$', blog.views.addlike),
    url(r'^article(?P<article_id>\d+)/addcomment/$', blog.views.addcomment),
    url(r'^article(?P<article_id>\d+)/$', blog.views.article),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^page(\d+)/$', blog.views.articles),
    url(r'^$', blog.views.articles),
]
