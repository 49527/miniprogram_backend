from rest_framework import serializers
from usersys.models import UserDeliveryInfo
from ordersys.models import OrderReasonBind
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice


class SubmitDeliveryInfoSerializer(serializers.ModelSerializer):
    user_sid = serializers.CharField(max_length=128)

    class Meta:
        model = UserDeliveryInfo
        fields = (
            "user_sid",
            "address", "contact", "house_number", "contact_pn"
        )


class CancelOrderSerializer(serializers.ModelSerializer):
    user_sid = serializers.CharField(max_length=128)

    class Meta:
        model = OrderReasonBind
        fields = (
            "user_sid",
            "reason", "order", "desc"
        )


class TypeQuantitySerializer(serializers.Serializer):
    p_type = serializers.PrimaryKeyRelatedField(
        queryset=ProductTopType.objects.filter(operator=top_type_choice.CONSUMER))
    quantity = serializers.FloatField(min_value=0)


class OneClickOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    type_quantity = TypeQuantitySerializer(many=True)
    deli_id = serializers.PrimaryKeyRelatedField(
        queryset=UserDeliveryInfo.objects.all()
    )


class CompeteOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)


class CancelOrder4BSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)
    reason = serializers.CharField(max_length=128)


class TypeQuantity4BSerializer(serializers.Serializer):
    p_type = serializers.IntegerField()
    quantity = serializers.FloatField(min_value=0)


class BookkeepingOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    oid = serializers.CharField(max_length=128)
    type_quantity = TypeQuantity4BSerializer(many=True)


class BookkeepingPnOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    pn = serializers.CharField(max_length=128)
    type_quantity = TypeQuantity4BSerializer(many=True)


class BookkeepingScanOrderSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)
    qr_info = serializers.CharField(max_length=128)
    type_quantity = TypeQuantity4BSerializer(many=True)