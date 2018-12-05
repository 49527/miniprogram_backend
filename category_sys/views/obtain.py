from rest_framework.views import APIView
from base.views import WLAPIView
from category_sys.serializers import ProductTopTypeSerializers
from category_sys.serializers.obtain_api import ObtainCategorySerializer
from category_sys.funcs import get_category_list


class CategoryListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainCategorySerializer(data=data)
        self.validate_serializer(seri)

        categorys = get_category_list(**seri.data)
        seri_order = ProductTopTypeSerializers(categorys, many=True)
        return self.generate_response(
            data={
                "categorys": seri_order.data,
            },
            context=context
        )

