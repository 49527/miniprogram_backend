from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType


class ProductSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = ('id', 'unit', 't_sub_name')

class ProductTopTypeSerializers(serializers.ModelSerializer):
    product_sub_type = ProductSubTypeSerializers(many=True)

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name", "product_sub_type")
