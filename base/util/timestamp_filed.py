import datetime
from rest_framework import serializers
from pytz import timezone


class TimestampField(serializers.Field):
    def to_representation(self, value):
        epoch = datetime.datetime(1970, 1, 1, tzinfo=timezone('UTC'))
        return int((value - epoch).total_seconds())
