from rest_framework import serializers
from ordersys.models import OrderInfo


class OrderDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderInfo
        fields = '__all__'
