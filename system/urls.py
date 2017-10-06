from django.conf.urls import include, url
import system.views

urlpatterns = [
    # Examples:
    # url(r'^article(?P<article_id>\d+)/addcomment/$', blog.views.addcomment),
    url(r'^country/json/$', system.views.country_json),
    url(r'^product/json/$', system.views.products_json),
    url(r'^measure/json/$', system.views.measure_json),
    url(r'^(.*)/(?P<product_id>\d+)/$', system.views.product_view),
    url(r'^(?P<category>\w+)/', system.views.category_view),

]
