# coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from usersys.models import UserBase
from business_sys.choices.model_choices import truck_state_choice


class Truck(models.Model):
    number_plate = models.CharField(_(u"车牌号"), max_length=20)
    start_time = models.DateTimeField(_(u"开始时间"))
    end_time = models.DateTimeField(_(u"结束时间"))
    amount = models.FloatField(_(u"金额"), default=0.0)
    quantity = models.FloatField(_(u"数量"), default=0.0)
    state = models.IntegerField(_(u"状态"), choices=truck_state_choice.choice, default=truck_state_choice.DEFAULT)

    def __unicode__(self):
        return self.number_plate


class TruckUserBind(models.Model):
    uid_b = models.ForeignKey(
        UserBase,
        related_name="truck_b",
        verbose_name=_(u"u回收员id"),
        null=True,
        blank=True
    )

    truck = models.ForeignKey(
        Truck,
        related_name="truck_o",
        verbose_name=_(u"装车单id"),
        null=True,
        blank=True
    )

    def __unicode__(self):
        return u"{}-{}".format(self.truck, self.uid_b)
