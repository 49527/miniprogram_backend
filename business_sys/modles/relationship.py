# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from business_sys.modles import RecycleBin
from business_sys.choices.model_choices import business_staff_status
from usersys.models import UserBase
from category_sys.models import ProductSubType


class BusinessStaffBind(models.Model):
    recycle_bin = models.ForeignKey(
        RecycleBin,
        verbose_name=_("回收站"),
        related_name="staff"
    )
    recycling_staff = models.ForeignKey(
        UserBase,
        verbose_name=_("回收员"),
        related_name="business"
    )
    business_staff_status = models.IntegerField(choices=business_staff_status.choice, default=0)


class BusinessProductTypeBind(models.Model):
    recycle_bin = models.ForeignKey(
        RecycleBin,
        verbose_name=_("回收站"),
        related_name="product_subtype"
    )
    p_type = models.ForeignKey(
        ProductSubType,
        verbose_name=_("二级品类"),
        related_name="business"
    )
    price = models.FloatField()
    modified_time = models.DateTimeField(auto_now=True)

