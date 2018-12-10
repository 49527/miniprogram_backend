from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.operate_api import SubmitDeliveryInfoSerializer, CancelOrderSerializer,\
    OneClickOrderSerializer, CompeteOrderSerializer, CancelOrder4BSerializer, BookkeepingOrderSerializer, \
    BookkeepingPnOrderSerializer, BookkeepingScanOrderSerializer
from ordersys.funcs.operate import submit_delivery_info, cancel_order, one_click_order, compete_order, cancel_order_b, \
    bookkeeping_order, bookkeeping_order_pn, bookkeeping_order_scan
from ordersys.serializers.order import OrderDisplaySerializer
from usersys.serializers.usermodel import UserDeliveryInfoDisplay


class SubmitDeliveryInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SubmitDeliveryInfoSerializer(data=data)
        self.validate_serializer(seri)

        addr = submit_delivery_info(**seri.data)
        seri_addr = UserDeliveryInfoDisplay(addr)

        return self.generate_response(
            data={
                "addr": seri_addr.data
            },
            context=context
        )


class CancelOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CancelOrderSerializer(data=data)
        self.validate_serializer(seri)

        cancel_order(**seri.validated_data)

        return self.generate_response(
            data={},
            context=context
        )


class OneClickOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = OneClickOrderSerializer(data=data)
        self.validate_serializer(seri)

        order = one_click_order(**seri.validated_data)

        seri_order = OrderDisplaySerializer(order)
        return self.generate_response(
            data={
                "order_info": seri_order.data
            },
            context=context
        )


class RecycleOrderCompeteView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CompeteOrderSerializer(data=data)
        self.validate_serializer(seri)

        order = compete_order(**seri.validated_data)
        seri_order = OrderDisplaySerializer(order)
        return self.generate_response(
            data={
                "order_info": seri_order.data
            },
            context=context
        )


class RecycleOrderCancelView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CancelOrder4BSerializer(data=data)
        self.validate_serializer(seri)

        cancel_order_b(**seri.validated_data)

        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = BookkeepingOrderSerializer(data=data)
        self.validate_serializer(seri)

        bookkeeping_order(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingPnOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = BookkeepingPnOrderSerializer(data=data)
        self.validate_serializer(seri)

        bookkeeping_order_pn(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingScanOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = BookkeepingScanOrderSerializer(data=data)
        self.validate_serializer(seri)

        bookkeeping_order_scan(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )
