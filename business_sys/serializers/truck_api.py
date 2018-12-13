from rest_framework import serializers


class GenerateLoadingCredentialSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    number_plate = serializers.CharField(max_length=128)


class ObtainLoadingCredentialSummarySerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
