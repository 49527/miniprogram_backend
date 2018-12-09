from rest_framework import serializers


class ObtainSelfInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
