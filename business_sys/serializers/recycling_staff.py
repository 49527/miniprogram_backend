from rest_framework import serializers
from business_sys.models import RecycleBin


class RecycleBinBasicInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecycleBin
        fields = (
            'rb_name',
            'r_b_type',
        )


class WrappedPhoneNumberField(serializers.CharField):

    def to_representation(self, value):
        value = super(WrappedPhoneNumberField, self).to_representation(value)
        if value is not None and len(value) >= 7:
            return value[0:3] + "****" + value[-4:]
        else:
            return value


class BusinessUserCenterSerializer(serializers.Serializer):
    pn = WrappedPhoneNumberField()
    total_amount = serializers.FloatField()
    recycle_bin = RecycleBinBasicInfoSerializer()


class UploadGpsSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    lat = serializers.FloatField()
    lng = serializers.FloatField()

