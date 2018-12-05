from django.conf.urls import url, include
from ordersys.views import obtain, operate


obtain_urls = [
    url(r'^order_list/$', obtain.ObtainOrderListView.as_view()),
    url(r'^overview/$', obtain.ObtainOverviewView.as_view()),
    url(r'^delivery_info/$', obtain.ObtainDeliveryInfoView.as_view()),
    url(r'^uncompleted/$', obtain.ObtainUncompletedOrderView.as_view()),
    url(r'^c_type/$', obtain.ObtainTopTypeCListView.as_view()),
    url(r'^cancel_reason/$', obtain.ObtainCancelReasonView.as_view()),
    url(r'^order_list_b/$', obtain.RecycleOrderListView.as_view()),
    url(r'^order_details_b/$', obtain.RecycleOrderDetailsView.as_view()),

]

operate_urls = [
    url(r'^submit_delivery_info/$', operate.SubmitDeliveryInfoView.as_view()),
    url(r'^cancel_order/$', operate.CancelOrderView.as_view()),
    url(r'one_click_order/$', operate.OneClickOrderView.as_view()),
    url(r'^order_compete_b/$', operate.RecycleOrderCompeteView.as_view()),
    url(r'^order_cancel_b/$', operate.RecycleOrderCancelView.as_view()),
    url(r'^order_bookkeeping_b/$', operate.BookkeepingOrderView.as_view()),
]


urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
    url(r"^operate/", include(operate_urls)),
]
