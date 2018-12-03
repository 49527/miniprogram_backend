# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordersys.choices.model_choices import order_state_choice
from usersys.models import UserBase
from category_sys.models import ProductTopType
from base.util.misc_validators import validators
from usersys.models import UserDeliveryInfo


class OrderInfo(models.Model):
    create_time = models.DateTimeField(_('订单创建时间'), auto_now_add=True)
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
    c_delivery_info = models.ForeignKey(
        UserDeliveryInfo,
        verbose_name=_("客户收货信息"),
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
    quantity = models.FloatField()


class OrderCancelReason(models.Model):
    in_use = models.BooleanField(default=True)
    reason = models.CharField(max_length=256)

    def __unicode__(self):
        return self.reason


class OrderReasonBind(models.Model):
    reason = models.ForeignKey(
        OrderCancelReason,
        related_name="order",
        verbose_name="对应订单",
        null=True,
        blank=True
    )
    order = models.ForeignKey(
        OrderInfo,
        related_name="cancel_reason",
        verbose_name="取消原因"
    )
    desc = models.TextField(_("具体描述"), null=True, blank=True)
