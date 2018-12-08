from rest_framework import serializers
from ordersys.models import OrderInfo


class OrderDetailApiSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects.all())


class CompletedOrderSummeryApiSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
