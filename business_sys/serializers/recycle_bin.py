from django.db.models import Min, Max
from rest_framework import serializers
from business_sys.models import RecycleBin
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice


class RecycleBinDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = RecycleBin
        fields = (
            "id", "GPS_L", "GPS_A", "rb_name", "r_b_type", "loc_desc", "pn"
        )

    def to_representation(self, instance):
        data = super(RecycleBinDisplaySerializer, self).to_representation(instance)
        type_list = []
        recycle_bin = instance
        for c_type in ProductTopType.objects.filter(operator=top_type_choice.CONSUMER, in_use=True):
            dic = {
                "type_id": c_type.id,
                "c_type": c_type.t_top_name,
                "min_price": recycle_bin.product_subtype.filter(
                    p_type__toptype_c=c_type,
                    p_type__in_use=True).aggregate(Min("price"))["price__min"],
                "max_price": recycle_bin.product_subtype.filter(
                    p_type__toptype_c=c_type,
                    p_type__in_use=True).aggregate(Max("price"))["price__max"],
                "unit": c_type.c_subtype.first().unit,
            }
            type_list.append(dic)
        data["type_list"] = type_list
        return data


class NearbyDisplaySerializer(serializers.Serializer):
    recycle_bin = RecycleBinDisplaySerializer()
    distance = serializers.FloatField()
