from rest_framework import serializers
from category_sys.models import ProductSubType
from category_sys.serializers.category import ProductTopTypeSerializer
from business_sys.models import BusinessProductTypeBind


class ProductInfoSerializer(serializers.ModelSerializer):

    relation_id = serializers.ReadOnlyField(source='id')

    class Meta:
        model = BusinessProductTypeBind
        fields = ('relation_id', 'price')


class BusinessProductSubTypeSerializer(serializers.ModelSerializer):

    business_bind = ProductInfoSerializer(many=True)

    class Meta:
        model = ProductSubType
        fields = ("id", "t_sub_name", 'unit', 'business_bind')


class BusinessProductTopTypeSerializer(ProductTopTypeSerializer):
    product_sub_type = BusinessProductSubTypeSerializer(many=True, source='pst_prefetch')

    def to_representation(self, instance):
        data = super(BusinessProductTopTypeSerializer, self).to_representation(instance)
        if "product_sub_type" in data:
            filtered_product_sub_type_data = filter(
                lambda x: "business_bind" in x and len(x["business_bind"]) == 1,
                data["product_sub_type"]
            )

            # Flatten
            # original: {'id': 0, 't_sub_name': 'iron', 'business_bind': [{'price': 100, 'unit': 0, 'relation_id': 1}]}
            # result: {'id': 0, 't_sub_name': 'iron', 'price': 100, 'unit': 0, 'relation_id': 1}
            filtered_product_sub_type_data = map(
                lambda x: dict(x, **x.pop("business_bind")[0]),
                filtered_product_sub_type_data
            )

            data["product_sub_type"] = filtered_product_sub_type_data
        return data
