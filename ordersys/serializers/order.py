from rest_framework import serializers
from django.conf import settings
from django.utils.timezone import now
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductType
from usersys.serializers.usermodel import UserDeliveryInfoDisplay
from base.util.timestamp_filed import TimestampField
from category_sys.serializers import ProductSubTypeSerializers
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
    recycling_staff = RecyclingStaffDisplay(source="uid_b")

    class Meta:
        model = OrderInfo
        fields = (
            "location", "recycling_staff",
            "id", "create_time", "o_state", "c_delivery_info",
            "time_remain",
            "amount",
        )

    def get_time_remain(self, obj):
        # type: (OrderInfo) -> int
        time_elapsed = now() - obj.create_time
        time_remain = max(0, int(settings.TIME_FOR_SET_ORDER - time_elapsed.total_seconds()))
        return time_remain


class CancelReasonDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderCancelReason
        fields = (
            "id", "reason",
        )


class OrderDetailsSerializer(serializers.ModelSerializer):

    p_type = ProductSubTypeSerializers()

    class Meta:
        model = OrderProductType
        fields = (
            "id",
            "quantity",
            "p_type",
            "price"
        )
