from django.conf.urls import url, include
from business_sys.views import obtain


obtain_urls =[
    url(r'nearby/$', obtain.ObtainNearbyRecycleBinView.as_view()),
    url(r'rb_detail/$', obtain.ObtainRecycleBinDetailView.as_view()),
]

urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
]
