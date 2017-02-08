from django.conf.urls import url
import stock.views

urlpatterns = [
    # Examples:
    url(r'^package/json/$', stock.views.package_json),
    # url(r'^admin/', include(admin.site.urls)),
    # url(r'^consignment/(?P<consignment_id>\d+)/edit/$', document.views.consignment_edit),
    # url(r'^consignment/(?P<consignment_id>\d+)/items/json/$', document.views.items_json),
    # url(r'^consignment/all/json/$', document.views.consignments_json),
    # url(r'^consignment/new/$', document.vi# url(r'^items/$', .views),ews.consignment_new),
    # url(r'^$', stock.views.all),
]
