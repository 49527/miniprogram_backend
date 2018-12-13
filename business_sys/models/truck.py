# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from usersys.models import UserBase
from category_sys.models import ProductSubType
from business_sys.models import RecycleBin
from business_sys.choices.model_choices import truck_state_choice


class Truck(models.Model):
    number_plate = models.CharField(_(u"车牌号"), max_length=20, unique=True, db_index=True)
    join_time = models.DateTimeField(auto_now_add=True)
    load = models.FloatField(default=0)
    state = models.IntegerField(_(u"状态"), choices=truck_state_choice.choice, default=truck_state_choice.DEFAULT)
    other_info = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.number_plate


class LoadingCredential(models.Model):
    uid_b = models.ForeignKey(
        UserBase,
        related_name="user_loading_cred",
        verbose_name=_("回收员"),
    )

    recycle_bin = models.ForeignKey(
        RecycleBin,
        verbose_name=_("回收站"),
        related_name="rb_loading_cred",
    )

    truck = models.ForeignKey(
        Truck,
        related_name="truck_loading_cred",
        verbose_name=_("车辆"),
    )

    created_date = models.DateTimeField(
        verbose_name=_("生成时间"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _("装车单")
        verbose_name_plural = _("装车单")

    def __unicode__(self):
        return u"id:{} {} {} {}".format(
            self.id,
            self.truck,
            self.uid_b,
            self.created_date
        )


class LoadingCredentialDetail(models.Model):

    credential = models.ForeignKey(
        LoadingCredential,
        verbose_name=_("装车单"),
        related_name="cred_detail",
    )

    category = models.ForeignKey(
        ProductSubType,
        verbose_name=_("品类"),
        on_delete=models.SET_NULL,
        null=True,
    )

    quantity = models.FloatField(
        verbose_name=_("数量"),
    )

    price = models.FloatField(
        verbose_name=_("收购总价"),
    )

    class Meta:
        verbose_name = _("装车单详情")
        verbose_name_plural = _("装车单详情")

    def __unicode__(self):
        return u"id:{} cre_id:{} category:{} count:{}, price:{}".format(
            self.id,
            self.credential.id,
            self.category,
            self.quantity,
            self.price
        )
