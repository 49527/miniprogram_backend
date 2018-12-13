from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers import operate_api, order as order_seri
from ordersys.funcs import operate
from usersys.serializers import usermodel


class SubmitDeliveryInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.SubmitDeliveryInfoSerializer(data=data)
        self.validate_serializer(seri)

        addr = operate.submit_delivery_info(**seri.data)
        seri_addr = usermodel.UserDeliveryInfoDisplay(addr)

        return self.generate_response(
            data={
                "addr": seri_addr.data
            },
            context=context
        )


class CancelOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.CancelOrderSerializer(data=data)
        self.validate_serializer(seri)

        operate.cancel_order(**seri.validated_data)

        return self.generate_response(
            data={},
            context=context
        )


class OneClickOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.OneClickOrderSerializer(data=data)
        self.validate_serializer(seri)

        order = operate.one_click_order(**seri.validated_data)

        seri_order = order_seri.OrderDisplaySerializer(order)
        return self.generate_response(
            data={
                "order_info": seri_order.data
            },
            context=context
        )


class RecycleOrderCompeteView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.CompeteOrderSerializer(data=data)
        self.validate_serializer(seri)

        order = operate.compete_order(**seri.validated_data)
        seri_order = order_seri.OrderDisplaySerializer(order)
        return self.generate_response(
            data={
                "order_info": seri_order.data
            },
            context=context
        )


class RecycleOrderCancelView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.CancelOrder4BSerializer(data=data)
        self.validate_serializer(seri)

        operate.cancel_order_b(**seri.validated_data)

        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.BookkeepingOrderSerializer(data=data)
        self.validate_serializer(seri)

        operate.bookkeeping_order(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingPnOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.BookkeepingPnOrderSerializer(data=data)
        self.validate_serializer(seri)

        operate.bookkeeping_order_pn(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )


class BookkeepingScanOrderView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = operate_api.BookkeepingScanOrderSerializer(data=data)
        self.validate_serializer(seri)

        operate.bookkeeping_order_scan(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )
