from rest_framework import serializers
from business_sys.models import RecycleBin
from business_sys.choices.model_choices import recycle_bin_type


class ObtainNearbyRecycleBinSerializer(serializers.Serializer):
    lng = serializers.FloatField(min_value=0, max_value=360)
    lat = serializers.FloatField(min_value=-90, max_value=90)


class ObtainRecycleBinSerializer(serializers.Serializer):
    lng = serializers.FloatField(min_value=0, max_value=360)
    lat = serializers.FloatField(min_value=-90, max_value=90)
    rb_id = serializers.PrimaryKeyRelatedField(
        queryset=RecycleBin.objects.filter(r_b_type=recycle_bin_type.FIXED)
    )
