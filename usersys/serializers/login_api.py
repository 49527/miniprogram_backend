from rest_framework import serializers
from base.util.misc_validators import validators


class LoginSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])


class SubmitPnSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])
    user_sid = serializers.CharField(max_length=127)


class PNvalidateSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20)
    sid = serializers.CharField(max_length=60)
    vcode = serializers.CharField(max_length=6)
    user_sid = serializers.CharField(max_length=128)


class LogoutSerializer(serializers.Serializer):
    user_sid = serializers.CharField(max_length=128)


class RecyclingStaffLoginSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])
    pwd = serializers.CharField(max_length=50)


class SendSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])


class ForgetPwdSerializer(serializers.Serializer):
    pn = serializers.CharField(max_length=20, validators=[validators.get_validator("phone number")])
    new_pwd1 = serializers.CharField(max_length=50)
    new_pwd2 = serializers.CharField(max_length=50)
    vcode = serializers.CharField(max_length=6)