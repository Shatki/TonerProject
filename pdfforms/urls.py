from django.conf.urls import url
import pdfforms.views
# from pdfforms.views import GeneratePDF


urlpatterns = [
    # Examples:
    url(r'^consignment/(?P<consignment_id>\d+)/print/pdf/$', pdfforms.views.torg12),
    # url(r'^consignment/1/print/pdf/$', GeneratePDF.as_view()),
    # url(r'^$', stock.views.all),
]
