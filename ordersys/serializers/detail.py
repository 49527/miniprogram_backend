from rest_framework import serializers
from ordersys.models import OrderProductType


class OrderDetailSerializer(serializers.ModelSerializer):

    t_name = serializers.ReadOnlyField(source='p_type.toptype_c.t_top_name')
    unit = serializers.ReadOnlyField(source='p_type.unit')
    tid = serializers.ReadOnlyField(source='p_type.toptype_c.id')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderProductType
        fields = (
            't_name',
            'quantity',
            'total_price',
            'unit',
            'tid',
        )

    def get_total_price(self, obj):
        return obj.quantity * obj.price


class CompletedOrderSummerySerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    tid = serializers.ReadOnlyField(source='p_type__toptype_c')
    t_name = serializers.ReadOnlyField(source='p_type__toptype_c__t_top_name')
    unit = serializers.ReadOnlyField(source='p_type__unit')
