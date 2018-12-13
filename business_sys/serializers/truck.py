from rest_framework import serializers
from base.util.timestamp_filed import TimestampField


class UnitQuantitySerializer(serializers.Serializer):
    unit = serializers.IntegerField()
    price = serializers.FloatField()
    quantity = serializers.FloatField()
    t_sub_name = serializers.CharField()
    t_top_name = serializers.CharField()


class LoadingCredentialSummarySerializer(serializers.Serializer):
    end_time = TimestampField()
    last_until_now = serializers.IntegerField()
    price = serializers.FloatField()
    quantity = UnitQuantitySerializer(many=True)
