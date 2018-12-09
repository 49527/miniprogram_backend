from rest_framework.views import APIView
from base.views import WLAPIView
from usersys.serializers.obtain_api import ObtainSelfInfoSerializer, ObtainRecyclingStaffInfoSerializer, \
    ObtainCheckQrInfoSerializer
from usersys.serializers.usermodel import UserInfoDisplay
from usersys.funcs.obtain import obtain_self_info, obtain_qr_info, obtain_self_info_b, checkout_qr_info


class ObtainSelfInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainSelfInfoSerializer(data=data)
        self.validate_serializer(seri)

        user_info, is_validate, n_times, total_amount = obtain_self_info(**seri.data)
        seri_u_info = UserInfoDisplay(user_info)
        return self.generate_response(
            data={
                "user_info": seri_u_info.data,
                "is_validate": is_validate,
                "n_times": n_times,
                "total_amount": total_amount
            },
            context=context
        )


class QRInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainSelfInfoSerializer(data=data)
        self.validate_serializer(seri)

        qr_info = obtain_qr_info(**seri.data)
        return self.generate_response(
            data={
                "qr_info": qr_info
            },
            context=context
        )


class CheckQRInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainCheckQrInfoSerializer(data=data)
        self.validate_serializer(seri)

        state = checkout_qr_info(**seri.data)
        return self.generate_response(
            data={
                "state": state
            },
            context=context
        )


class ObtainRecyclingStaffInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainRecyclingStaffInfoSerializer(data=data)
        self.validate_serializer(seri)

        pn, total_amount = obtain_self_info_b(**seri.data)
        return self.generate_response(
            data={
                "pn": pn,
                "total_amount": total_amount
            },
            context=context
        )
