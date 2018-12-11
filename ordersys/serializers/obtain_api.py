from rest_framework import serializers
from base.util.timestamp_filed import TimestampField
from ordersys.models import OrderInfo


class ObtainOrderListSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class ObtainOverviewSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainDeliveryInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainUncompletedorderSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainOrderDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects.all())


class RecycleOrderListSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class RecycleOrderDetailsSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)


class ObtainOrderListDateSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    start_date = TimestampField()
    end_date = TimestampField()


class ObtainOrderListCountSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainOrderListTypeSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    o_type = serializers.IntegerField()


class ObtainOrderListStateSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    o_state = serializers.IntegerField()
