from django.conf.urls import url
import dashboard.views
import document.views

urlpatterns = [
    # Examples:
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/edit/$', document.views.document_edit),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/save/$', document.views.document_save),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/delete/$', document.views.document_delete),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/item/add/$', document.views.document_item_add),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/item/paste/$', document.views.document_item_paste),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/item/(?P<item_id>\d+)/edit/$', document.views.document_item_edit),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/item/(?P<item_id>\d+)/delete/$', document.views.document_item_delete),
    url(r'^(?P<document>\w+)/(?P<document_id>\d+)/items/json/$', document.views.document_items_json),
    url(r'^(?P<document>\w+)/all/$', document.views.documents),
    url(r'^(?P<document>\w+)/all/json/$', document.views.documents_json),
    url(r'^(?P<document>\w+)/(?P<date_from>\d+)/json/$', document.views.documents_json),
    url(r'^(?P<document>\w+)/(?P<date_from>\d+)/(?P<date_to>\d+)/json/$', document.views.documents_json),
    url(r'^(?P<document>\w+)/new/$', document.views.document_new),
    url(r'^(?P<document>\w+)/$', document.views.documents),
    # url(r'^$', stock.views.all),
]
