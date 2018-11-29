# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordersys.choices.state_choices import order_state_choice
from usersys.models import UserBase


class OrderInfo(models.Model):
    create_time = models.DateTimeField(_('订单创建时间'), auto_now_add=True)
    location = models.CharField(max_length=100)
    amount = models.FloatField(_("订单金额"), default=0.0)
    o_state = models.IntegerField(_("订单状态"), choices=order_state_choice.choice)
    uid = models.ForeignKey(
        UserBase,
        related_name="order",
        verbose_name=_("用户id"),
    )
