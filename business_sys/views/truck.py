from rest_framework.views import APIView
from base.views import WLAPIView
from business_sys.serializers.truck import (
    LoadingCredentialSummarySerializer
)
from business_sys.serializers.truck_api import GenerateLoadingCredentialSerializer, ObtainLoadingCredentialSummarySerializer
from business_sys.funcs.truck import get_truck_info, create_truck_info


class ObtainTruckOrderInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainLoadingCredentialSummarySerializer(data=data)
        self.validate_serializer(seri)

        truck = LoadingCredentialSummarySerializer(get_truck_info(**seri.data))
        return self.generate_response(
            data=truck.data,
            context=context
        )


class CreateTruckOrderInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = GenerateLoadingCredentialSerializer(data=data)
        self.validate_serializer(seri)

        cred = create_truck_info(**seri.data)
        return self.generate_response(
            data={"credential_id": cred.id},
            context=context
        )
