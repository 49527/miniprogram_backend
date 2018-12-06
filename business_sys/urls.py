from django.conf.urls import url, include

from business_sys.views import obtain, operate


obtain_urls = [
    url(r'^product_price_list/$', obtain.CategoryPriceListView.as_view()),
    url(r'nearby/$', obtain.ObtainNearbyRecycleBinView.as_view()),
    url(r'rb_detail/$', obtain.ObtainRecycleBinDetailView.as_view()),
]

operate_urls = [
    url(r'^product_price_update/$', operate.CategoryPriceUpdateView.as_view()),
]


urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
    url(r"^operate/", include(operate_urls)),
]
