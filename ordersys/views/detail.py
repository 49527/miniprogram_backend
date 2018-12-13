from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.funcs import order_detail as user_detail_funcs
from ordersys.serializers import detail as detail_seri, detail_api


class OrderDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = detail_api.OrderDetailApiSerializer(data=data)
        self.validate_serializer(seri)

        order_details = user_detail_funcs.get_order_detail(**seri.validated_data)

        return self.generate_response(
            data={
                "details": detail_seri.OrderDetailSerializer(order_details, many=True).data
            },
            context=context
        )


class CompletedOrderSummaryView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = detail_api.CompletedOrderSummeryApiSerializer(data=data)
        self.validate_serializer(seri)

        summary = user_detail_funcs.get_orders_summary_c(**seri.validated_data)

        return self.generate_response(
            data={
                "summary": detail_seri.CompletedOrderSummerySerializer(summary, many=True).data
            },
            context=context
        )
