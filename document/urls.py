from django.conf.urls import include, url
from django.contrib import admin
import authentication.views
import document.views

urlpatterns = [
    # Examples:
    url(r'^consignment/(?P<consignment_id>\d+)/edit/$', document.views.consignment_edit),
    url(r'^consignment/(?P<consignment_id>\d+)/save/$', document.views.consignment_save),
    url(r'^consignment/(?P<consignment_id>\d+)/delete/$', document.views.consignment_delete),
    url(r'^consignment/(?P<consignment_id>\d+)/item/add/$', document.views.consignment_item_add),
    url(r'^consignment/(?P<consignment_id>\d+)/item/(?P<item_id>\d+)/edit/$', document.views.consignment_item_edit),
    url(r'^consignment/(?P<consignment_id>\d+)/item/(?P<item_id>\d+)/delete/$', document.views.consignment_item_delete),
    url(r'^consignment/(?P<consignment_id>\d+)/items/json/$', document.views.consignment_items_json),
    url(r'^consignment/all/$', document.views.consignments),
    url(r'^consignment/all/json/$', document.views.consignments_json),
    url(r'^consignment/new/$', document.views.consignment_new),
    url(r'^consignment/$', document.views.consignments),
    # url(r'^$', stock.views.all),
]
