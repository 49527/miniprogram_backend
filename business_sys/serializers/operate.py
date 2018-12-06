from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType
from business_sys.models import BusinessProductTypeBind


class TypePriceSerializer(serializers.Serializer):
    pst_id = serializers.CharField(max_length=128)
    price = serializers.FloatField(min_value=0)


class BusinessProductTypeUpdateSerializers(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    type_price = TypePriceSerializer(many=True)


class ProductSubTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = (
            "id", "t_sub_name", "unit", "price"
        )


class ProductTopTypeSerializers(serializers.ModelSerializer):
    product_sub_type = ProductSubTypeSerializers(many=True)

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name", "product_sub_type")