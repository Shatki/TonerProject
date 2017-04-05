"""TonerProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import homepage.views
import authentication.views
import dashboard.views
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'toner.views.home', name='home'),
    url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('authentication.urls')),
    url(r'^catalog/', include('system.urls')),
    url(r'^dashboard/', dashboard.views.dashboard),
    url(r'^document/', include('document.urls')),
    url(r'^form/', include('pdfforms.urls')),
    url(r'^stock/', include('stock.urls')),
    url(r'^system/', include('system.urls')),
    # url(r'^test/', dashboard.views.testpage),
    url(r'^(?P<nickname>\w+)/photo$', authentication.views.get_photo),
    url(r'^(?P<nickname>\w+)$', authentication.views.dispatch_user),
    url(r'^$', homepage.views.home_page),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
