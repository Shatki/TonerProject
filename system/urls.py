from django.conf.urls import include, url
import system.views

urlpatterns = [
    # Examples:
    # url(r'^article(?P<article_id>\d+)/addcomment/$', blog.views.addcomment),
    url(r'^(.*)/(?P<product_id>\d+)/$', system.views.product_view),
    url(r'^(?P<category>\w+)/', system.views.category_view),

]
