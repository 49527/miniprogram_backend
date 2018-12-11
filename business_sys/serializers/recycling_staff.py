from rest_framework import serializers
from business_sys.models import RecycleBin


class RecycleBinBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecycleBin
        fields = (
            'rb_name',
            'r_b_type',
        )


class BusinessUserCenterSerializer(serializers.Serializer):
    pn = serializers.CharField()
    total_amount = serializers.FloatField()
    recycle_bin = RecycleBinBasicInfoSerializer()


class UploadGpsSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    lat = serializers.FloatField()
    lng = serializers.FloatField()

