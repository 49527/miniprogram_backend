from rest_framework import serializers
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductType
from usersys.serializers.usermodel import UserDeliveryInfoDisplay
from base.util.timestamp_filed import TimestampField
from category_sys.models import ProductTopType, ProductSubType
from category_sys.serializers import ProductTopTypeSerializers, ProductSubTypeSerializers


class OrderDisplaySerializer(serializers.ModelSerializer):
    c_delivery_info = UserDeliveryInfoDisplay()
    location = serializers.ReadOnlyField(source="c_delivery_info.address")
    create_time = TimestampField()

    class Meta:
        model = OrderInfo
        fields = (
            "location",
            "id", "create_time", "o_state", "c_delivery_info"
        )


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