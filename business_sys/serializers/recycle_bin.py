from django.db.models import Min, Max, Prefetch
from rest_framework import serializers
from base.util.timestamp import datetime_to_timestamp
from business_sys.models import RecycleBin, BusinessProductTypeBind
from category_sys.models import ProductTopType, ProductSubType
from category_sys.choices.model_choices import top_type_choice
from business_sys.serializers.recycle_product import BusinessProductTopTypeSerializer


class RecycleBinDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = RecycleBin
        fields = (
            "id", "GPS_L", "GPS_A", "rb_name", "r_b_type", "loc_desc", "pn"
        )

    def to_representation(self, instance):
        data = super(RecycleBinDisplaySerializer, self).to_representation(instance)
        type_list = []
        for c_type in ProductTopType.objects.filter(operator=top_type_choice.CONSUMER, in_use=True):
            try:
                unit = c_type.c_subtype.filter(in_use=True).first().unit
            except AttributeError:
                unit = None

            dic = {
                "type_id": c_type.id,
                "c_type": c_type.t_top_name,
                "min_price": instance.product_subtype.filter(
                    p_type__toptype_c=c_type,
                    p_type__in_use=True).aggregate(Min("price"))["price__min"],
                "max_price": instance.product_subtype.filter(
                    p_type__toptype_c=c_type,
                    p_type__in_use=True).aggregate(Max("price"))["price__max"],
                "unit": unit
            }
            type_list.append(dic)
        data["type_list"] = type_list
        return data


class RecycleBinBusinessPriceDisplaySerializer(serializers.ModelSerializer):

    last_update = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()

    class Meta:
        model = RecycleBin
        fields = (
            "id", "rb_name", "r_b_type", "loc_desc", "pn", "last_update", "categories"
        )

    def get_last_update(self, obj):
        # type: (RecycleBin) -> int
        return datetime_to_timestamp(
            obj.product_subtype.aggregate(Max("modified_time"))["modified_time__max"]
        )

    def get_categories(self, obj):
        queryset = ProductTopType.objects.filter(operator=top_type_choice.BUSINESS).prefetch_related(
            Prefetch(
                'b_subtype',
                queryset=ProductSubType.objects.filter(in_use=True).prefetch_related(
                    Prefetch(
                        'business',
                        queryset=BusinessProductTypeBind.objects.filter(recycle_bin=obj),
                        to_attr='business_bind')
                ),
                to_attr='pst_prefetch')
        )
        return BusinessProductTopTypeSerializer(queryset, many=True).data


class NearbyDisplaySerializer(serializers.Serializer):
    recycle_bin = RecycleBinDisplaySerializer()
    distance = serializers.FloatField()
