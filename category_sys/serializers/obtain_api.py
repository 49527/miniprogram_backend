from rest_framework import serializers


class ObtainCategorySerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)