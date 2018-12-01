# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

from base.util.misc_validators import validators
from usersys.choices.model_choice import user_validate_status, user_role_choice


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, openid, password, **extra_fields):
        if openid is None:
            raise ValueError('The openid must be set')

        user = self.model(openid=openid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, openid, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(openid, password, **extra_fields)

    def create_superuser(self, openid, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(openid, password, **extra_fields)


class UserBase(AbstractBaseUser, PermissionsMixin):
    openid = models.CharField(_('微信用户唯一标识'), max_length=50, unique=True)
    pn = models.CharField(_('电话号码'), max_length=25, null=True, validators=[
        validators.get_validator("phone number")
    ])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    nickname = models.CharField(max_length=128)
    nickname_modified = models.BooleanField(default=False)
    role = models.IntegerField(_("用户角色"), choices=user_role_choice.choice)

    object = UserManager()
    USERNAME_FIELD = 'openid'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('userbase')
        verbose_name_plural = _('usersbase')

    def get_short_name(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname


class UserValidate(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="user_validate",
        verbose_name=_("用户id"),
    )
    idcard_number = models.CharField(_("身份证号"), max_length=30)
    name = models.CharField(_("真实姓名"), max_length=30)
    validate_status = models.IntegerField(_("验证状态"), choices=user_validate_status.choice)


class RecyclingStaffInfo(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="recycling_staff_info",
        verbose_name=_("用户id"),
    )
    rs_name = models.CharField(_("回收员姓名"), max_length=30)
    number_plate = models.CharField(max_length=20)
