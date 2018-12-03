from rest_framework import serializers
from ordersys.models import OrderInfo, OrderCancelReason
from usersys.serializers.usermodel import UserDeliveryInfoDisplay


class OrderDisplaySerializer(serializers.ModelSerializer):
    c_delivery_info = UserDeliveryInfoDisplay()
    location = serializers.ReadOnlyField(source="c_delivery_info.address")

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
