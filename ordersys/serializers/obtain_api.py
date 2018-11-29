from rest_framework import serializers


class ObtainOrderListSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class ObtainOverviewSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)