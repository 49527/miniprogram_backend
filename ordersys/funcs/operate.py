# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserDeliveryInfo
from ordersys.models import OrderReasonBind, OrderProductTypeBind, OrderInfo, OrderCancel, OrderProductType
from ordersys.choices.model_choices import order_state_choice
from ordersys.funcs.utils import get_uncompleted_order
from category_sys.models import ProductSubType
from business_sys.models import BusinessProductTypeBind

@user_from_sid(Error404)
def submit_delivery_info(user, **data):
    return UserDeliveryInfo.objects.create(uid=user,**data)


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
def one_click_order(user, **data):
    if not get_uncompleted_order(user).count() == 0:
        raise WLException(403, _("已经存在一个未完成订单"))
    delivery_info = data["deli_id"]
    if not delivery_info.uid == user:
        raise WLException(402, _("用户收货地址不存在"))
    order = OrderInfo.objects.create(
        uid_c=user,
        c_delivery_info=delivery_info,
        o_state=order_state_choice.CREATED
    )
    for dic in data["type_quantity"]:
        OrderProductTypeBind.objects.create(oid=order, **dic)

    return order


@user_from_sid(Error404)
def compete_order(user, oid):
    order = OrderInfo.objects.filter(id=oid).first()
    if order.uid_b is not None:
        raise WLException(400, "订单已被抢")
    if order.uid_b is user:
        raise WLException(401, "不可重复抢单")
    if order.o_state == order_state_choice.CREATED:
        order.uid_b = user
        order.o_state = order_state_choice.ACCEPTED
        order.save()
    return order


@user_from_sid(Error404)
def cancel_order_b(user, oid, reason):
    order = OrderInfo.objects.filter(id=oid).first()
    if order.o_state == order_state_choice.CANCELED or order.o_state == order_state_choice.COMPLETED:
        raise WLException(400, "此订单已完成或者已被取消，不能执行此操作")
    if order.uid_b != user:
        raise WLException(401, "这个订单不属于该用户,不能执行此操作")

    order.uid_b = None
    order.o_state = order_state_choice.CREATED
    order.save()
    OrderCancel.objects.create(
        reason=reason,
        order=order
    )


@user_from_sid(Error404)
def bookkeepingorder(user, oid, **data):

    type_quantity = data.get("type_quantity")
    for i in type_quantity:
        p_id = i.get("p_type")
        order = OrderInfo.objects.filter(id=oid).first()
        p_type = ProductSubType.objects.filter(id=p_id).first()
        bpt = BusinessProductTypeBind.objects.filter(p_type=p_type).first()
        if bpt is None:
            raise WLException(401, "品类不存在，清添加后操作")
        if OrderProductType.objects.filter(p_type=p_type, oid=order).first():
            continue
        OrderProductType.objects.create(
            p_type=p_type,
            oid=order,
            quantity=i.get("quantity"),
            price=bpt.price
        )
    return True
