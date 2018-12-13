from rest_framework import serializers
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from base.util.timestamp import datetime_to_timestamp
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductType, OrderProductTypeBind
from usersys.serializers.usermodel import UserDeliveryInfoDisplay
from base.util.timestamp_filed import TimestampField
from category_sys.serializers.category import NestedProductSubTypeSerializer, ProductTopTypeSerializer
from usersys.models import UserBase


class RecyclingStaffDisplay(serializers.ModelSerializer):
    rs_pn = serializers.ReadOnlyField(source="pn")
    rs_name = serializers.ReadOnlyField(source="recycling_staff_info.rs_name")

    class Meta:
        model = UserBase
        fields = (
            "rs_name", "rs_pn"
        )


class TimeSerializer(serializers.Serializer):
    time = TimestampField()


class OrderDisplaySerializer(serializers.ModelSerializer):
    c_delivery_info = UserDeliveryInfoDisplay()
    location = serializers.ReadOnlyField(source="c_delivery_info.address")
    create_time = TimestampField()
    time_remain = serializers.SerializerMethodField()
    time_remain_b = serializers.SerializerMethodField()
    recycling_staff = RecyclingStaffDisplay(source="uid_b")
    target_time = serializers.SerializerMethodField()
    distance = serializers.ReadOnlyField()

    class Meta:
        model = OrderInfo
        fields = (
            "location", "recycling_staff",
            "id", "create_time", "o_state", "c_delivery_info",
            "time_remain",
            "time_remain_b",
            "amount",
            "target_time",
            'can_cancel_b',
            "distance",
        )

    def get_time_remain(self, obj):
        # type: (OrderInfo) -> int
        time_elapsed = now() - obj.create_time
        time_remain = max(0, int(settings.TIME_FOR_SET_ORDER - time_elapsed.total_seconds()))
        return time_remain

    def get_time_remain_b(self, obj):
        # type: (OrderInfo) -> int
        time_elapsed = now() - obj.create_time
        time_remain = max(0, int(settings.COUNTDOWN_FOR_ORDER - time_elapsed.total_seconds()))
        return time_remain

    def get_target_time(self, obj):
        return datetime_to_timestamp(obj.create_time) + settings.COUNTDOWN_FOR_ORDER


class CancelReasonDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderCancelReason
        fields = (
            "id", "reason",
        )


class OrderDetailsSubTypeSerializer(serializers.ModelSerializer):

    sub_type = NestedProductSubTypeSerializer(source="p_type")

    class Meta:
        model = OrderProductType
        fields = (
            "quantity",
            "sub_type",
            "price",
        )


class OrderDetailsSerializer(serializers.ModelSerializer):

    delivery_info = UserDeliveryInfoDisplay(source="c_delivery_info")
    sub_type = OrderDetailsSubTypeSerializer(many=True, source="order_detail_b")
    distance = serializers.ReadOnlyField()

    class Meta:
        model = OrderInfo
        fields = ("amount", "delivery_info", "sub_type", 'distance')


class OrderCustomerSubmittedProductSerializer(serializers.ModelSerializer):

    p_type = ProductTopTypeSerializer()
    budget = serializers.SerializerMethodField()

    class Meta:
        model = OrderProductTypeBind
        fields = (
            'quantity',
            'p_type',
            'budget',
        )

    def get_budget(self, obj):
        # type: (OrderProductTypeBind) -> float
        attr_budget = getattr(obj, 'budget', None)
        if attr_budget is not None:
            return attr_budget
        else:
            if obj.oid.recycle_bin is not None:
                # Recycle bin bind, get budget of that bin.
                budget = obj.oid.recycle_bin.product_subtype.filter(
                    p_type__toptype_c=obj.p_type,
                    p_type__in_use=True,
                ).aggregate(
                    budget=models.Avg("price")
                )["budget"]

            else:
                # Recycle bin not bind, get budget of all recycle bin.
                budget = obj.p_type.c_subtype.filter(in_use=True).aggregate(
                    budget=models.Avg("business__price")
                )["budget"]

            return budget * obj.quantity if budget is not None else 0


class OrderCDetailsSerializer(serializers.ModelSerializer):

    delivery_info = UserDeliveryInfoDisplay(source="c_delivery_info")
    customer_submitted_products = OrderCustomerSubmittedProductSerializer(many=True, source="order_detail_c")

    class Meta:
        model = OrderInfo
        fields = ("amount", "delivery_info", "customer_submitted_products")
