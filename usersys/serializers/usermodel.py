from rest_framework import serializers
from usersys.models import UserValidate, UserBase, UserDeliveryInfo


class UserInfoDisplay(serializers.ModelSerializer):
    idcard_number = serializers.ReadOnlyField(source="user_validate.idcard_number")
    name = serializers.ReadOnlyField(source="user_validate.name")

    class Meta:
        model = UserBase
        fields = (
            "id", "pn", "name", "idcard_number"
        )


class UserDeliveryInfoDisplay(serializers.ModelSerializer):

    class Meta:
        model = UserDeliveryInfo
        fields = (
            "id", "address", "contact", "house_number", "contact_pn", "lat", "lng", "is_analysis"
        )
