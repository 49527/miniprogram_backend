from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.operate_api import SubmitDeliveryInfoSerializer, CancelOrderSerializer,\
    OneClickOrderSerializer
from ordersys.funcs.operate import submit_delivery_info, cancel_order, one_click_order


class SubmitDeliveryInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SubmitDeliveryInfoSerializer(data=data)
        self.validate_serializer(seri)

        submit_delivery_info(**seri.data)

        return self.generate_response(
            data={},
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

        one_click_order(**seri.validated_data)

        return self.generate_response(
            data={},
            context=context
        )
