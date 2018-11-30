from rest_framework import serializers
from usersys.models import UserValidate, UserBase


class UserInfoDisplay(serializers.ModelSerializer):
    idcard_number = serializers.ReadOnlyField(source="user_validate.idcard_number")
    name = serializers.ReadOnlyField(source="user_validate.name")

    class Meta:
        model = UserBase
        fields = (
            "id", "pn", "name", "idcard_number"
        )