from rest_framework import serializers
from base.util.timestamp_filed import TimestampField
from ordersys.models import OrderInfo
from ordersys.choices.model_choices import order_state_choice
from business_sys.choices.model_choices import recycle_bin_type


class ObtainOrderListSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class ObtainOverviewSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainDeliveryInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainUncompletedorderSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainOrderDetailSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.PrimaryKeyRelatedField(queryset=OrderInfo.objects.all())


class RecycleOrderListSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    lat = serializers.FloatField(allow_null=True, default=None)
    lng = serializers.FloatField(allow_null=True, default=None)


class RecycleOrderDetailsSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)


class ObtainOrderListDateSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    start_date = TimestampField()
    end_date = TimestampField()


class ObtainOrderListCountSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainOrderListTypeSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    o_type = serializers.ChoiceField(choices=recycle_bin_type.choice)


class ObtainOrderListStateSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    o_state = serializers.ChoiceField(choices=order_state_choice.choice)


class ObtainOrderComplexFilterSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    o_state = serializers.ChoiceField(choices=order_state_choice.choice, allow_null=True, default=None)
    o_type = serializers.ChoiceField(choices=recycle_bin_type.choice, allow_null=True, default=None)
    start_date = TimestampField(allow_null=True, default=None)
    end_date = TimestampField(allow_null=True, default=None)
    lat = serializers.FloatField(allow_null=True, default=None)
    lng = serializers.FloatField(allow_null=True, default=None)
