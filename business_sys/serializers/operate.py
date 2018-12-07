from rest_framework import serializers
from category_sys.models import ProductTopType, ProductSubType
from business_sys.models import BusinessProductTypeBind


class TypePriceSerializer(serializers.Serializer):
    pst_id = serializers.CharField(max_length=128)
    price = serializers.FloatField(min_value=0)


class BusinessProductTypeUpdateSerializers(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    type_price = TypePriceSerializer(many=True)


class BusinessSerializer(serializers.Serializer):
    rb_id = serializers.CharField(max_length=128)


class BusinessPriceSerializer(serializers.ModelSerializer):
    t_sub_id = serializers.ReadOnlyField(source='p_type.id')
    t_sub_name = serializers.ReadOnlyField(source='p_type.t_sub_name')
    p_top_name = serializers.ReadOnlyField(source='p_type.toptype_b.t_top_name')
    p_top_id = serializers.ReadOnlyField(source='p_type.toptype_b.id')
    unit = serializers.ReadOnlyField(source="p_type.unit")

    def to_representation(self, instance):
        ret = super(BusinessPriceSerializer, self).to_representation(instance)
        return ret

    class Meta:
        model = BusinessProductTypeBind
        fields = (
            't_sub_id',
            't_sub_name',
            'p_top_name',
            "p_top_id",
            'unit',
            'price',
            'modified_time'
        )


class ProductTopTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductTopType
        fields = ("id", "t_top_name")