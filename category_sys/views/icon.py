from rest_framework.views import APIView
from base.views import WLBinaryView
from category_sys.serializers.category_api import ObtainTopTypePhotoApiSerializer
from category_sys.funcs.icon import obtain_top_type_photo


class ObtainCategoryIconView(WLBinaryView, APIView):

    def get_io_stream(self, data, context):
        seri = ObtainTopTypePhotoApiSerializer(data=data)
        self.validate_serializer(seri)
        return obtain_top_type_photo(**seri.validated_data), 'image'
