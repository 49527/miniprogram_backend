from rest_framework import serializers
from category_sys.models import ProductTopType


class ObtainTopTypePhotoApiSerializer(serializers.Serializer):
    top_type = serializers.PrimaryKeyRelatedField(queryset=ProductTopType.objects.filter(in_use=True))
