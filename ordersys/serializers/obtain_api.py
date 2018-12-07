from rest_framework import serializers


class ObtainOrderListSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class ObtainOverviewSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainDeliveryInfoSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class ObtainUncompletedorderSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class RecycleOrderListSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)


class RecycleOrderDetailsSerilaizer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)


class ObtainOrderListDateSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    page = serializers.IntegerField(default=0)
    start_date = serializers.DateField()
    end_date = serializers.DateField()


class ObtainOrderListCountSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
