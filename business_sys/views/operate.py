from rest_framework.views import APIView
from base.views import WLAPIView
from business_sys.serializers import BusinessProductTypeUpdateSerializers, CheckValidateCodeSerializers
from business_sys.funcs import update_price, check_validate_code


class CategoryPriceUpdateView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = BusinessProductTypeUpdateSerializers(data=data)
        self.validate_serializer(seri)
        update_price(**seri.validated_data)
        return self.generate_response(
            data={
            },
            context=context
        )


class CheckValidateCodeView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CheckValidateCodeSerializers(data=data)
        self.validate_serializer(seri)
        state = check_validate_code(**seri.validated_data)
        return self.generate_response(
            data={
                "state": state
            },
            context=context
        )
