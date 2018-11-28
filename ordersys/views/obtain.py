from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.obtain_api import ObtainOrderListSerializer, ObtainOverviewSerializer
from ordersys.funcs.obtain import obtain_order_list, obtain_overview
from ordersys.serializers.Order import OrderDisplaySerializer


class ObtainOrderListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages = obtain_order_list(count_per_page=5, **seri.data)
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages
            },
            context=context
        )

class ObtainOverviewView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOverviewSerializer(data=data)
        self.validate_serializer(seri)

        n_times, total_amount = obtain_overview(**seri.data)
        return self.generate_response(
            data={
                "n_times": n_times,
                "total_amount": total_amount
            },
            context=context
        )
