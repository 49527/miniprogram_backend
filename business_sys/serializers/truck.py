from rest_framework import serializers


class ObtainTruckOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class TruckOrderInfoSerializer(serializers.Serializer):
    end_time = serializers.DateTimeField()
    time_diff = serializers.CharField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()


class CreateTruckOrderInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    number_plate = serializers.CharField(max_length=128)
