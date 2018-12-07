from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType


class ProductTopTypeOrderSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name")


class ProductSubTypeSerializers(serializers.ModelSerializer):
    t_top_name = serializers.ReadOnlyField(source="toptype_b.t_top_name")

    class Meta:
        model = ProductSubType
        fields = ("id", "t_sub_name", "t_top_name")


class ProductTopTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name")
