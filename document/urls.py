from django.conf.urls import include, url
from django.contrib import admin
import authentication.views
import document.views

urlpatterns = [
    # Examples:
    # url(r'^article(?P<article_id>\d+)/addlike/$', blog.views.addlike),
    # url(r'^article(?P<article_id>\d+)/addcomment/$', blog.views.addcomment),
    # url(r'^article(?P<article_id>\d+)/$', blog.views.article),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^consignment/(?P<consignment_id>\d+)/edit/$', document.views.consignment_edit),
    url(r'^consignment/(?P<consignment_id>\d+)/items/json/$', document.views.items_json),
    url(r'^consignment/all/$', document.views.consignments),
    url(r'^consignment/all/json/$', document.views.consignments_json),
    url(r'^consignment/new/$', document.views.consignment_new),
    url(r'^consignment/$', document.views.consignments),
    # url(r'^$', stock.views.all),
]
