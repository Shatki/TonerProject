from django.conf.urls import include, url
import stock.views

urlpatterns = [
    # Examples:
    # url(r'^article(?P<article_id>\d+)/addlike/$', blog.views.addlike),
    # url(r'^article(?P<article_id>\d+)/addcomment/$', blog.views.addcomment),
    # url(r'^article(?P<article_id>\d+)/$', blog.views.article),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^consignment/(?P<consignment_id>\d+)/edit/$', document.views.consignment_edit),
    # url(r'^consignment/(?P<consignment_id>\d+)/items/json/$', document.views.items_json),
    url(r'^item/all/json/$', stock.views.items_json),
    # url(r'^consignment/all/json/$', document.views.consignments_json),
    # url(r'^consignment/new/$', document.views.consignment_new),
    # url(r'^items/$', .views),
    # url(r'^$', stock.views.all),
]
