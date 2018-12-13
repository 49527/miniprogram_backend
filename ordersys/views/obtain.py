from rest_framework.views import APIView
from base.views import WLAPIView
from ordersys.serializers import obtain_api, order as order_seri
from ordersys.funcs import obtain as obtain_funcs
from ordersys.choices.model_choices import order_state_choice
from usersys.serializers import usermodel
from django.conf import settings
COUNT_PER_PAGE = settings.COUNT_PER_PAGE


class ObtainOrderListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.ObtainOrderListSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list(count_per_page=COUNT_PER_PAGE, **seri.data)
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
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
        seri = obtain_api.ObtainOverviewSerializer(data=data)
        self.validate_serializer(seri)

        n_times, total_amount = obtain_funcs.obtain_overview(**seri.data)
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
        seri = obtain_api.ObtainDeliveryInfoSerializer(data=data)
        self.validate_serializer(seri)

        delivery_info, address_exist, pn = obtain_funcs.obtain_delivery_info(**seri.data)
        seri_info = usermodel.UserDeliveryInfoDisplay(delivery_info)
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
        seri = obtain_api.ObtainUncompletedorderSerilaizer(data=data)
        self.validate_serializer(seri)

        uncompleted, exist = obtain_funcs.obtain_uncompleted(**seri.data)

        seri_info = order_seri.OrderDisplaySerializer(uncompleted)

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
        seri = obtain_api.ObtainOrderDetailSerializer(data=data)
        self.validate_serializer(seri)

        order_info = obtain_funcs.obtain_order_detail(**seri.data)

        seri_info = order_seri.OrderDisplaySerializer(order_info)

        return self.generate_response(
            data={
                "order_info": seri_info.data,
            },
            context=context
        )


class ObtainTopTypeCListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        toptypes, modified_time = obtain_funcs.obtain_c_toptype_list()

        seri_time = order_seri.TimeSerializer({"time": modified_time})

        return self.generate_response(
            data={
                "c_types": toptypes,
                "modified_time": seri_time.data
            },
            context=context
        )


class ObtainCancelReasonCView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        reasons = obtain_funcs.obtain_cancel_reason_c()
        seri_reasons = order_seri.CancelReasonDisplaySerializer(reasons, many=True)

        return self.generate_response(
            data={
                "reasons": seri_reasons.data
            },
            context=context
        )


class ObtainCancelReasonBView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)

        reasons = obtain_funcs.obtain_cancel_reason_b()
        seri_reasons = order_seri.CancelReasonDisplaySerializer(reasons, many=True)

        return self.generate_response(
            data={
                "reasons": seri_reasons.data
            },
            context=context
        )


class RecycleOrderListView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.RecycleOrderListSerilaizer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list_by_complex_filter(
            count_per_page=COUNT_PER_PAGE,
            o_state=order_state_choice.CREATED,
            **seri.validated_data
        )
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
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
        seri = obtain_api.RecycleOrderDetailsSerilaizer(data=data)
        self.validate_serializer(seri)
        orders = obtain_funcs.obtain_order_details(**seri.data)
        seri_order = order_seri.OrderDetailsSerializer(orders)
        return self.generate_response(
            data={
                "orders": seri_order.data,
            },
            context=context
        )


class RecycleOrderCustomerDetailsView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.RecycleOrderDetailsSerilaizer(data=data)
        self.validate_serializer(seri)
        orders = obtain_funcs.obtain_order_details_with_budget(**seri.data)
        seri_order = order_seri.OrderCDetailsSerializer(orders)
        return self.generate_response(
            data={
                "orders": seri_order.data,
            },
            context=context
        )


class ObtainOrderListDateView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.ObtainOrderListDateSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list_by_complex_filter(
            count_per_page=COUNT_PER_PAGE, **seri.validated_data
        )
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
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
        seri = obtain_api.ObtainOrderListCountSerializer(data=data)
        self.validate_serializer(seri)

        orders = obtain_funcs.obtain_order_count(**seri.data)
        return self.generate_response(
            data={
                "orders": orders
            },
            context=context
        )


class ObtainOrderListTypeView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.ObtainOrderListTypeSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list_by_complex_filter(
            count_per_page=COUNT_PER_PAGE, **seri.validated_data
        )
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
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
        seri = obtain_api.ObtainOrderListStateSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list_by_complex_filter(
            count_per_page=COUNT_PER_PAGE, **seri.validated_data
        )
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count
            },
            context=context
        )


class ObtainOrderListComplexFilterView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = obtain_api.ObtainOrderComplexFilterSerializer(data=data)
        self.validate_serializer(seri)

        orders, n_pages, count = obtain_funcs.obtain_order_list_by_complex_filter(
            count_per_page=5, **seri.validated_data
        )
        seri_order = order_seri.OrderDisplaySerializer(orders, many=True)
        return self.generate_response(
            data={
                "orders": seri_order.data,
                "n_pages": n_pages,
                "count": count
            },
            context=context
        )
