# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from business_sys.models import RecycleBin
from business_sys.choices.model_choices import business_staff_status
from usersys.models import UserBase
from category_sys.models import ProductSubType


class RecyclingStaffInfo(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="recycling_staff_info",
        verbose_name=_("用户id"),
    )
    rs_name = models.CharField(_("回收员姓名"), max_length=30)
    number_plate = models.CharField(_("车牌号"), max_length=20)
    staff_status = models.IntegerField(
        choices=business_staff_status.choice,
        default=business_staff_status.DEFAULT
    )
    recycle_bin = models.ForeignKey(
        RecycleBin,
        related_name="recycling_staff",
        verbose_name=_("回收站")
    )

    def __unicode__(self):
        return self.rs_name


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

    def __unicode__(self):
        return u"{} - {}: RMB: {}".format(self.recycle_bin, self.p_type, self.price)


class RecyclingStaffInfoGps(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="staff_info_gps",
        verbose_name=_("用户id"),
    )
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    create_time = models.DateTimeField(_('创建时间'), auto_now_add=True)

    def __unicode__(self):
        return u"{}-{}-{}".format(self.uid, self.lat, self.lng)
