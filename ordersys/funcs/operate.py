# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserDeliveryInfo
from ordersys.models import OrderReasonBind, OrderProductTypeBind, OrderInfo
from ordersys.choices.model_choices import order_state_choice
from ordersys.funcs.utils import get_uncompleted_order


@user_from_sid(Error404)
def submit_delivery_info(user, **data):
    UserDeliveryInfo.objects.create(uid=user,**data)


@user_from_sid(Error404)
def cancel_order(user, **data):
    order = data["order"]

    if not order.uid_c == user:
        raise WLException(403, _("这个订单不属于该用户"))
    if order.o_state == order_state_choice.CANCELED or order.o_state == order_state_choice.COMPLETED:
        raise WLException(403, _("此订单已完成或者已被取消，不能执行此操作"))
    if data.get("reason", None) is None and data.get("desc", None) is None:
        raise WLException(402, _("reason或者desc中至少有一个字段不能为空"))

    OrderReasonBind.objects.create(**data)
    order.o_state = order_state_choice.CANCELED
    order.save()


@user_from_sid(Error404)
def one_click_order(user, contact_pn, type_quantity):
    if not get_uncompleted_order(user).count() == 0:
        raise WLException(403, "there exist a order uncompleted")
    order = OrderInfo.objects.create(uid_c=user, contact_pn_c=contact_pn, o_state=order_state_choice.CREATED)
    for dic in type_quantity:
        OrderProductTypeBind.objects.create(oid=order, **dic)

    return order
