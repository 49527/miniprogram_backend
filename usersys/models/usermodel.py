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

    def _create_user(self, internal_name, password, **extra_fields):
        if internal_name is None:
            raise ValueError('The openid must be set')

        user = self.model(internal_name=internal_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, internal_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(internal_name, password, **extra_fields)

    def create_superuser(self, internal_name, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(internal_name, password, **extra_fields)

    def set_password(self, internal_name, password):
        user = self.get(internal_name=internal_name)
        user.set_password(password)
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    internal_name = models.CharField(_("内部登录名称"), max_length=64, unique=True)
    pn = models.CharField(_('电话号码'), max_length=25, null=True, validators=[
        validators.get_validator("phone number")
    ])
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    role = models.IntegerField(_("用户角色"), choices=user_role_choice.choice)

    objects = UserManager()
    USERNAME_FIELD = 'internal_name'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('userbase')
        verbose_name_plural = _('usersbase')

    def get_short_name(self):
        return u"{} - {}".format(self.internal_name, self.pn)

    def get_full_name(self):
        return u"{} - {}".format(self.internal_name, self.pn)


class WechatUserContext(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="user_wechat_context",
        verbose_name=_("用户id"),
    )
    openid = models.CharField(_('微信用户唯一标识'), max_length=50, unique=True)
    nickname = models.CharField(max_length=128)
    nickname_modified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.openid


class UserValidate(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="user_validate",
        verbose_name=_("用户id"),
    )
    idcard_number = models.CharField(_("身份证号"), max_length=30)
    name = models.CharField(_("真实姓名"), max_length=30)
    validate_status = models.IntegerField(_("验证状态"), choices=user_validate_status.choice)

    def __unicode__(self):
        return self.idcard_number


class UserDeliveryInfo(models.Model):
    uid = models.ForeignKey(
        UserBase,
        related_name="user_delivery_info",
        verbose_name=_("用户id"),
    )
    address = models.TextField(_("收货地址"))
    contact = models.CharField(_("联系人"), max_length=30, null=True, blank=True)
    house_number = models.CharField(_("门牌号"), max_length=20, null=True, blank=True)
    contact_pn = models.CharField(_('联系电话'), max_length=25, validators=[
        validators.get_validator("phone number")
    ])
    in_use = models.BooleanField(default=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    can_resolve_gps = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} {} {} {}".format(self.address, self.house_number, self.contact, self.contact_pn)
