from rest_framework.views import APIView
from base.views import WLAPIView
from business_sys.serializers.obtain_api import ObtainNearbyRecycleBinSerializer, ObtainRecycleBinSerializer
from business_sys.funcs.obtain import obtain_nearby_recycle_bin, obtain_recycle_bin_detail
from business_sys.serializers.recycle_bin import NearbyDisplaySerializer, RecycleBinDisplaySerializer


class ObtainNearbyRecycleBinView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainNearbyRecycleBinSerializer(data=data)
        self.validate_serializer(seri)

        p_list = obtain_nearby_recycle_bin(**seri.data)

        seri_p = NearbyDisplaySerializer(p_list, many=True)

        return self.generate_response(
            data={
                "closest": seri_p.data
            },
            context=context
        )


class ObtainRecycleBinDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainRecycleBinSerializer(data=data)
        self.validate_serializer(seri)

        rb, distance = obtain_recycle_bin_detail(**seri.data)

        seri_rb = RecycleBinDisplaySerializer(rb)

        return self.generate_response(
            data={
                "recycle_bin": seri_rb.data,
                "distance": distance
            },
            context=context
        )