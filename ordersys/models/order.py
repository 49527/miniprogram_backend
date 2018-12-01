# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordersys.choices.state_choices import order_state_choice
from usersys.models import UserBase
from category_sys.models import ProductTopType


class OrderInfo(models.Model):
    create_time = models.DateTimeField(_('订单创建时间'), auto_now_add=True)
    location = models.TextField(null=True, blank=True)
    amount = models.FloatField(_("订单金额"), default=0.0)
    o_state = models.IntegerField(_("订单状态"), choices=order_state_choice.choice)
    uid_c = models.ForeignKey(
        UserBase,
        related_name="order_c",
        verbose_name=_("客户id"),
        null=True,
        blank=True
    )
    uid_b = models.ForeignKey(
        UserBase,
        related_name="order_b",
        verbose_name=_("回收员id"),
        null=True,
        blank=True
    )


class OrderProductTypeBind(models.Model):
    p_type = models.ForeignKey(
        ProductTopType,
        verbose_name=_("C端客户对应顶级品类"),
        related_name="order"
    )
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("订单id"),
        related_name="product_type"
    )
