from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType


class ProductSubTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = ("id", "t_sub_name")


class ProductTopTypeSerializers(serializers.ModelSerializer):
    # product_sub_type = ProductSubTypeSerializers(many=True).data

    def to_representation(self, instance):
        ret = super(ProductTopTypeSerializers, self).to_representation(instance)
        ret["product_sub_type"] = ProductSubTypeSerializers(many=True).data
        return ret

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name")