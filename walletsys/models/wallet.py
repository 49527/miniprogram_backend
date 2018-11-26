# coding=UTF-8
from __future__ import unicode_literals
from walletsys.choice.transaction_choice import transaction_type
from django.utils.translation import ugettext_lazy as _
from django.db import models
from usersys.models import UserBase
from ordersys.models import OrderInfo


class Balance(models.Model):
    uid = models.ForeignKey(
        UserBase,
        related_name="Balance",
        verbose_name=_("用户id"),
    )
    balance = models.FloatField()

class TransactionDetail(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    transaction_type = models.IntegerField(_("收支类型"), choices=transaction_type.choice)
    amount = models.FloatField(_("收支金额")),
    oid = models.ForeignKey(
        OrderInfo,
        related_name="Transaction_Detail",
        verbose_name=_("响应订单"),
        null=True
    )
    uid = models.ForeignKey(
        UserBase,
        related_name="Transaction_Detail",
        verbose_name=_("用户id"),
    )
