from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType


class ProductSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = ('id', 'unit', 't_sub_name')


class NestedProductTopTypeSerializer(serializers.ModelSerializer):
    product_sub_type = ProductSubTypeSerializer(many=True)

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name", "product_sub_type")


class ProductTopTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name")


class NestedProductSubTypeSerializer(serializers.ModelSerializer):
    toptype_c = ProductTopTypeSerializer()
    toptype_b = ProductTopTypeSerializer()

    class Meta:
        model = ProductSubType
        fields = ('id', 'unit', 't_sub_name', 'toptype_c', 'toptype_b')
