# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from base.util.misc_validators import validators
from usersys.models import UserBase, UserDeliveryInfo
from usersys.choices.model_choice import user_role_choice
from ordersys.choices.model_choices import order_state_choice
from category_sys.models import ProductTopType, ProductSubType
from business_sys.models import RecycleBin


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
    pn = models.CharField(_('电话号码'), max_length=25, null=True, blank=True, validators=[
        validators.get_validator("phone number")
    ])

    recycle_bin = models.ForeignKey(
        RecycleBin,
        verbose_name=_("回收站"),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u"{}:{} vs {}".format(self.id, self.uid_c, self.uid_b)

    @property
    def can_cancel_b(self):
        return self.budget_amount < settings.BUDGET_MAX_CAN_CANCEL

    # TODO: FILL NEXT 2 PROPERTY
    @property
    def can_cancel_c(self):
        return True

    @property
    def budget_amount(self):
        type_binds = self.order_detail_c.all()
        amount = 0
        recycling_staff = self.uid_b
        if recycling_staff is None:
            return None
        for type_bind in type_binds:
            price = recycling_staff.recycling_staff_info.recycle_bin.product_subtype.filter(
                p_type__toptype_c=type_bind.p_type,
                p_type__in_use=True).aggregate(models.Min("price"))["price__min"]
            price = 0 if price is None else price
            amount += price * type_bind.quantity
        return amount


class OrderProductTypeBind(models.Model):
    p_type = models.ForeignKey(
        ProductTopType,
        verbose_name=_("C端客户对应顶级品类"),
        related_name="order_bind_c"
    )
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("订单id"),
        related_name="order_detail_c"
    )
    quantity = models.FloatField()

    def __unicode__(self):
        return u"[{}] - {}, count:{}".format(self.oid, self.p_type, self.quantity)


class OrderProductType(models.Model):
    p_type = models.ForeignKey(
        ProductSubType,
        verbose_name=_("B端客户对应商品"),
        related_name="order_bind_b"
    )
    oid = models.ForeignKey(
        OrderInfo,
        verbose_name=_("订单id"),
        related_name="order_detail_b"
    )
    quantity = models.FloatField()
    price = models.FloatField()

    def __unicode__(self):
        return u"[{}] - {}, count:{}".format(self.oid, self.p_type, self.quantity)


class OrderCancelReason(models.Model):
    in_use = models.BooleanField(default=True)
    reason = models.CharField(max_length=256)
    reason_type = models.IntegerField(choices=user_role_choice.choice)

    def __unicode__(self):
        return self.reason


class OrderCancelReasonBind(models.Model):
    reason = models.ForeignKey(
        OrderCancelReason,
        related_name="order",
        verbose_name=_("对应订单"),
        null=True,
        blank=True
    )
    order = models.OneToOneField(
        OrderInfo,
        related_name="cancel_reason",
        verbose_name=_("取消原因")
    )
    desc = models.TextField(_("具体描述"), null=True, blank=True)

    def __unicode__(self):
        return u"[{}] - {}, desc: {}".format(self.order, self.reason, self.desc)
