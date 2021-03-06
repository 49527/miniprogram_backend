from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers.obtain_api import ObtainOrderListSerializer, ObtainOverviewSerializer,\
    ObtainDeliveryInfoSerializer, ObtainUncompletedorderSerilaizer, RecycleOrderListSerilaizer, \
    RecycleOrderDetailsSerilaizer, ObtainOrderListDateSerializer, ObtainOrderListCountSerializer, \
    ObtainOrderDetailSerializer, ObtainOrderListTypeSerializer, ObtainOrderListStateSerializer
from ordersys.funcs.obtain import obtain_order_list, obtain_overview, obtain_delivery_info, obtain_uncompleted,\
    obtain_c_toptype_list, obtain_cancel_reason, obtain_order_list_by_o_state, obtain_order_details, obtain_order_list_b,\
    obtain_order_count, obtain_order_detail, obtain_order_list_by_o_type, obtain_order_list_by_state
from ordersys.serializers.order import OrderDisplaySerializer, CancelReasonDisplaySerializer, OrderDetailsSerializer, TimeSerializer
from usersys.serializers.usermodel import UserDeliveryInfoDisplay


class ObtainOrderListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_order_list(count_per_page=5, **seri.data)
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count,
            },
            context=context
        )


class ObtainOverviewView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOverviewSerializer(data=data)
        self.validate_serializer(seri)

        n_times, total_amount = obtain_overview(**seri.data)
        return self.generate_response(
            data={
                "n_times": n_times,
                "total_amount": total_amount
            },
            context=context
        )


class ObtainDeliveryInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainDeliveryInfoSerializer(data=data)
        self.validate_serializer(seri)

        delivery_info, address_exist, pn = obtain_delivery_info(**seri.data)
        seri_info = UserDeliveryInfoDisplay(delivery_info)
        return self.generate_response(
            data={
                "delivery_info": seri_info.data,
                "address_exist": address_exist,
                "pn": pn
            },
            context=context
        )


class ObtainUncompletedOrderView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainUncompletedorderSerilaizer(data=data)
        self.validate_serializer(seri)

        uncompleted, exist = obtain_uncompleted(**seri.data)

        seri_info = OrderDisplaySerializer(uncompleted)

        return self.generate_response(
            data={
                "uncompleted": seri_info.data,
                "exist": exist
            },
            context=context
        )


class ObtainOrderDetailView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderDetailSerializer(data=data)
        self.validate_serializer(seri)

        order_info = obtain_order_detail(**seri.data)

        seri_info = OrderDisplaySerializer(order_info)

        return self.generate_response(
            data={
                "order_info": seri_info.data,
            },
            context=context
        )


class ObtainTopTypeCListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        toptypes, modified_time = obtain_c_toptype_list()

        seri_time = TimeSerializer({"time": modified_time})

        return self.generate_response(
            data={
                "c_types": toptypes,
                "modified_time": seri_time.data
            },
            context=context
        )


class ObtainCancelReasonView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        reasons = obtain_cancel_reason()
        seri_reasons = CancelReasonDisplaySerializer(reasons, many=True)

        return self.generate_response(
            data={
                "reasons": seri_reasons.data
            },
            context=context
        )


class RecycleOrderListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = RecycleOrderListSerilaizer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_order_list_by_o_state(count_per_page=5, page=seri.data["page"])
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count,
            },
            context=context
        )


class RecycleOrderDetailsView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = RecycleOrderDetailsSerilaizer(data=data)
        self.validate_serializer(seri)
        orders, distance = obtain_order_details(**seri.data)
        seri_order = OrderDetailsSerializer(orders)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "distance": distance
            },
            context=context
        )


class ObtainOrderListDateView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListDateSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_order_list_b(count_per_page=5, **seri.validated_data)
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count,
            },
            context=context
        )


class ObtainOrderListCountView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListCountSerializer(data=data)
        self.validate_serializer(seri)

        orders = obtain_order_count(**seri.data)
        return self.generate_response(
            data={
                "orders": orders
            },
            context=context
        )


class ObtainOrderListTypeView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListTypeSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_order_list_by_o_type(count_per_page=5, **seri.validated_data)
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count
            },
            context=context
        )


class ObtainOrderListStateView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainOrderListStateSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_order_list_by_state(count_per_page=5, **seri.validated_data)
        seri_order = OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count
            },
            context=context
        )
