from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType


class ProductSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = ('id', 'unit', 't_sub_name')


class ProductTopTypeSerializer(serializers.ModelSerializer):
    product_sub_type = ProductSubTypeSerializer(many=True)

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name", "product_sub_type")
