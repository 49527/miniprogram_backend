from rest_framework import serializers
from django.conf import settings
from django.core.cache import caches
from django.utils.timezone import now
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductType
from usersys.serializers.usermodel import UserDeliveryInfoDisplay
from base.util.timestamp_filed import TimestampField
from category_sys.serializers.category import ProductSubTypeSerializer
from usersys.models import UserBase
from business_sys.funcs.utils.positon import get_one_to_one_distance


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

    class Meta:
        model = OrderInfo
        fields = (
            "location", "recycling_staff",
            "id", "create_time", "o_state", "c_delivery_info",
            "time_remain",
            "time_remain_b",
            "amount",
            'can_cancel',
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


class CancelReasonDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderCancelReason
        fields = (
            "id", "reason",
        )


class OrderDetailsSubTypeSerializer(serializers.ModelSerializer):

    sub_type = ProductSubTypeSerializer(source="p_type")

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

    class Meta:
        model = OrderInfo
        fields = ("amount", "delivery_info", "sub_type")


class OrderCDetailsSerializer(serializers.ModelSerializer):

    delivery_info = UserDeliveryInfoDisplay(source="c_delivery_info")
    customer_submitted_products = OrderDetailsSubTypeSerializer(many=True, source="order_detail_c")

    class Meta:
        model = OrderInfo
        fields = ("amount", "delivery_info", "customer_submitted_products")
