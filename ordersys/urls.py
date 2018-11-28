from django.conf.urls import url, include
from ordersys.views import obtain


obtain_urls = [
    url(r'^order_list/$', obtain.ObtainOrderListView.as_view()),
    url(r'^overview/$', obtain.ObtainOverviewView.as_view()),
]


urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
]
