from rest_framework.views import APIView
from base.views import WLAPIView
from business_sys.serializers.obtain_api import ObtainRecyclingStaffInfoApiSerializer
from business_sys.serializers.recycling_staff import BusinessUserCenterSerializer, UploadGpsSerializer
from business_sys.funcs.user_center import obtain_self_info_b, upload_gps


class ObtainRecyclingStaffInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainRecyclingStaffInfoApiSerializer(data=data)
        self.validate_serializer(seri)

        seri_result = BusinessUserCenterSerializer(obtain_self_info_b(**seri.data))

        return self.generate_response(
            data=seri_result.data,
            context=context
        )


class UploadGps(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = UploadGpsSerializer(data=data)
        self.validate_serializer(seri)

        upload_gps(**seri.validated_data)
        return self.generate_response(
            data={},
            context=context
        )

