from django.conf.urls import url, include
from ordersys.views import obtain, operate, detail


obtain_urls = [
    url(r'^order_list/$', obtain.ObtainOrderListView.as_view()),
    url(r'^overview/$', obtain.ObtainOverviewView.as_view()),
    url(r'^delivery_info/$', obtain.ObtainDeliveryInfoView.as_view()),
    url(r'^uncompleted/$', obtain.ObtainUncompletedOrderView.as_view()),
    url(r'^order_details_c/$', obtain.ObtainOrderDetailView.as_view()),
    url(r'^c_type/$', obtain.ObtainTopTypeCListView.as_view()),
    url(r'^cancel_reason/$', obtain.ObtainCancelReasonView.as_view()),
    url(r'^order_list_b/$', obtain.RecycleOrderListView.as_view()),
    url(r'^order_details_b/$', obtain.RecycleOrderDetailsView.as_view()),
    url(r'^order_details_customer/$', obtain.RecycleOrderCustomerDetailsView.as_view()),
    url(r'^order_list_by_date/$', obtain.ObtainOrderListDateView.as_view()),
    url(r'^order_list_count/$', obtain.ObtainOrderListCountView.as_view()),
    url(r'^order_list_by_type/$', obtain.ObtainOrderListTypeView.as_view()),
    url(r'^order_list_by_state/$', obtain.ObtainOrderListStateView.as_view()),

]

operate_urls = [
    url(r'^submit_delivery_info/$', operate.SubmitDeliveryInfoView.as_view()),
    url(r'^cancel_order/$', operate.CancelOrderView.as_view()),
    url(r'one_click_order/$', operate.OneClickOrderView.as_view()),
    url(r'^order_compete_b/$', operate.RecycleOrderCompeteView.as_view()),
    url(r'^order_cancel_b/$', operate.RecycleOrderCancelView.as_view()),
    url(r'^order_bookkeeping_b/$', operate.BookkeepingOrderView.as_view()),
    url(r'^order_bookkeeping_pn/$', operate.BookkeepingPnOrderView.as_view()),
    url(r'^order_bookkeeping_scan/$', operate.BookkeepingScanOrderView.as_view()),
]


detail_urls = [
    url(r'^detail/$', detail.OrderDetailView.as_view()),
    url(r'^summary/$', detail.CompletedOrderSummaryView.as_view()),
]


c_urls = [
    url(r'^detail/', include(detail_urls)),
]


b_urls = [
]

urlpatterns = [
    url(r'^obtain/', include(obtain_urls)),
    url(r"^operate/", include(operate_urls)),
    url(r'^c/', include(c_urls)),
    url(r'^b/', include(b_urls)),
]
