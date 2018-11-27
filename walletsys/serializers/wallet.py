from rest_framework import serializers
from walletsys.models import TransactionDetail


class TransactionDetailDisplay(serializers.ModelSerializer):

    class Meta:
        model = TransactionDetail
        fields = '__all__'
