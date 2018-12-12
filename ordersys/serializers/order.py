from rest_framework import serializers
from django.conf import settings
from django.utils.timezone import now
from base.util.timestamp import datetime_to_timestamp
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
    target_time = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

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
            "distance"
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

    def get_distance(self, obj):
        # type: (OrderInfo) -> int
        user_b_gps=self.context.get("user_b_gps")
        lat_c = obj.c_delivery_info.lat
        lng_c = obj.c_delivery_info.lng
        if obj.c_delivery_info.can_resolve_gps:
            if user_b_gps is not None:
                lat_b = user_b_gps['lat']
                lng_b = user_b_gps['lng']
                distance = get_one_to_one_distance(lat=lat_b, lng=lng_b, GPS_L=lng_c, GPS_A=lat_c)
            else:
                distance = None
        else:
            distance = None
        return distance


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
