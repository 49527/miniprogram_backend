from rest_framework.views import APIView
from base.views import WLAPIView
from business_sys.serializers.truck import (
                                            TruckOrderInfoSerializer,
                                            ObtainTruckOrderSerializer,
                                            CreateTruckOrderInfoSerializer)
from business_sys.funcs.truck import get_truck_info, create_truck_info


class ObtainTruckOrderInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainTruckOrderSerializer(data=data)
        self.validate_serializer(seri)

        truck = TruckOrderInfoSerializer(get_truck_info(**seri.data))
        return self.generate_response(
            data=truck.data,
            context=context
        )


class CreateTruckOrderInfoView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = CreateTruckOrderInfoSerializer(data=data)
        self.validate_serializer(seri)

        cred = create_truck_info(**seri.data)
        return self.generate_response(
            data={"credential_id": cred.id},
            context=context
        )
