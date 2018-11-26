from rest_framework import serializers


class ObtainBalanceSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainHistorySerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=60)
    page = serializers.IntegerField(default=0)
