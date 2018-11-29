from rest_framework import serializers
from base.util.timestamp_filed import TimestampField
from walletsys.models import TransactionDetail


class TransactionDetailDisplay(serializers.ModelSerializer):

    create_time = TimestampField()

    class Meta:
        model = TransactionDetail
        fields = '__all__'
