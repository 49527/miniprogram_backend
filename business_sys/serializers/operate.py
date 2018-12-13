from rest_framework import serializers


class TypePriceSerializer(serializers.Serializer):
    pst_id = serializers.CharField(max_length=128)
    price = serializers.FloatField(min_value=0)


class BusinessProductTypeUpdateSerializers(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    type_price = TypePriceSerializer(many=True)
    validate_code = serializers.CharField()


class CheckValidateCodeSerializers(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    validate_code = serializers.CharField()
