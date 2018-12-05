from rest_framework.views import APIView
from base.views import WLAPIView
from category_sys.serializers import ProductTopTypeSerializers
from business_sys.funcs import get_category_list


class CategoryPriceListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        categorys = get_category_list()
        seri_order = ProductTopTypeSerializers(categorys, many=True)
        return self.generate_response(
            data={
                "categorys": seri_order.data,
            },
            context=context
        )
