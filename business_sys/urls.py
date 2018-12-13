from django.conf.urls import url, include
from business_sys.views import obtain, operate, user_center


obtain_urls =[
    url(r'nearby/$', obtain.ObtainNearbyRecycleBinView.as_view()),
    url(r'rb_detail/$', obtain.ObtainRecycleBinDetailView.as_view()),
]


operate_urls = [
    url(r'^check_validate_code/$', operate.CheckValidateCodeView.as_view()),
    url(r'^product_price_update/$', operate.CategoryPriceUpdateView.as_view()),
]


b_urls = [
    url(r'^user_center/$', user_center.ObtainRecyclingStaffInfoView.as_view()),
    url(r'^rb_product_detail/$', obtain.ObtainRecycleBinPriceListView.as_view()),
    url(r'^upload_gps/$', user_center.UploadGps.as_view()),
]


urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
    url(r"^operate/", include(operate_urls)),
    url(r'^b/', include(b_urls)),
]
