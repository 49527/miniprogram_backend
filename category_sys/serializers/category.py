from rest_framework import serializers
from category_sys.models import ProductSubType


class ProductSubTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSubType
        fields = ('unit', 't_sub_name')
