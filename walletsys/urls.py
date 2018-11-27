from django.conf.urls import url, include
from walletsys.views import obtain

obtain_urls = [
    url(r'^balance/$', obtain.ObtainBalanceView.as_view()),
    url(r'^history/$', obtain.ObtainHistoryView.as_view()),
]

urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
]
