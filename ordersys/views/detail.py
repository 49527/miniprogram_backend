from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.funcs.order_detail import get_order_detail, get_orders_summary_c
from ordersys.serializers.detail import OrderDetailSerializer, CompletedOrderSummerySerializer
from ordersys.serializers.detail_api import OrderDetailApiSerializer, CompletedOrderSummeryApiSerializer


class OrderDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = OrderDetailApiSerializer(data=data)
        self.validate_serializer(seri)

        order_details = get_order_detail(**seri.validated_data)

        return self.generate_response(
            data={
                "details": OrderDetailSerializer(order_details, many=True).data
            },
            context=context
        )


class CompletedOrderSummaryView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = CompletedOrderSummeryApiSerializer(data=data)
        self.validate_serializer(seri)

        summary = get_orders_summary_c(**seri.validated_data)

        return self.generate_response(
            data={
                "summary": CompletedOrderSummerySerializer(summary, many=True).data
            },
            context=context
        )
