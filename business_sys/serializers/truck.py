from rest_framework import serializers
from base.util.timestamp_filed import TimestampField


class ObtainTruckOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class TruckOrderInfoSerializer(serializers.Serializer):
    end_time = TimestampField()
    time_diff = serializers.IntegerField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()


class CreateTruckOrderInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    number_plate = serializers.CharField(max_length=128)
