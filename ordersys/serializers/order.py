from rest_framework import serializers
from ordersys.models import OrderInfo, OrderCancelReason


class OrderDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = '__all__'


class CancelReasonDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderCancelReason
        fields = '__all__'
