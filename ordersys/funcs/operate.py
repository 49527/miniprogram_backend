# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserDeliveryInfo, UserBase
from ordersys.models import OrderReasonBind, OrderProductTypeBind, OrderInfo, OrderCancel, OrderProductType
from ordersys.choices.model_choices import order_state_choice
from ordersys.funcs.utils import get_uncompleted_order
from category_sys.models import ProductSubType
from business_sys.models import BusinessProductTypeBind
from usersys.choices.model_choice import user_role_choice


@user_from_sid(Error404)
def submit_delivery_info(user, **data):
    return UserDeliveryInfo.objects.create(uid=user, **data)


@user_from_sid(Error404)
def cancel_order(user, order, reason=None, desc=None, **kwargs):

    if not order.uid_c == user:
        raise WLException(403, _("这个订单不属于该用户"))
    if order.o_state == order_state_choice.CANCELED or order.o_state == order_state_choice.COMPLETED:
        raise WLException(403, _("此订单已完成或者已被取消，不能执行此操作"))
    if reason is None and desc is None:
        raise WLException(402, _("reason或者desc中至少有一个字段不能为空"))

    cancel_reason = OrderReasonBind.objects.create(order=order, reason=reason, **kwargs)
    cancel_reason.desc = cancel_reason.reason.reason if desc is None else cancel_reason.reason.reason
    cancel_reason.save()
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
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(407, "订单不存在")
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, "无权限操作")
    o_state = order.o_state
    if o_state == order_state_choice.ACCEPTED:
        raise WLException(402, "订单已接单")
    if o_state == order_state_choice.CANCELED:
        raise WLException(403, "订单被取消")
    if o_state == order_state_choice.COMPLETED:
        raise WLException(405, "订单已完成")
    if order.uid_b is not None:
        raise WLException(400, "订单已被抢")
    if order.o_state == order_state_choice.CREATED:
        order.uid_b = user
        order.o_state = order_state_choice.ACCEPTED
        order.save()
    return order


@user_from_sid(Error404)
def cancel_order_b(user, oid, reason):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, "无权限操作")
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(407, "订单不存在")
    if order.o_state in (order_state_choice.CANCELED, order_state_choice.COMPLETED):
        raise WLException(400, "此订单已完成或者已被取消，不能执行此操作")
    if order.uid_b != user:
        raise WLException(402, "这个订单不属于该用户,不能执行此操作")

    order.o_state = order_state_choice.CANCELED
    order.save()
    OrderCancel.objects.create(
        reason=reason,
        order=order
    )


@user_from_sid(Error404)
def bookkeeping_order(user, oid, type_quantity):
    price = 0.0
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, "无权限操作")
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(407, "订单不存在")
    if order.o_state != order_state_choice.ACCEPTED:
        raise WLException(405, "该订单未被接单，不能执行此操作")
    for i in type_quantity:
        p_id = i.get("p_type")
        p_type = ProductSubType.objects.filter(id=p_id).first()
        if p_type is None:
            raise WLException(402, "品类不存在，清添加后操作")
        bpt = BusinessProductTypeBind.objects.filter(p_type=p_type).first()
        if bpt is None:
            raise WLException(403, "回收站对应的商品不存在，清添加后操作")
        if OrderProductType.objects.filter(p_type=p_type, oid=order).first():
            continue
        OrderProductType.objects.create(
            p_type=p_type,
            oid=order,
            quantity=i.get("quantity"),
            price=bpt.price
        )
        price_ = bpt.price * i.get("quantity")
        price += price_
    order.amount = price
    order.o_state = order_state_choice.COMPLETED
    order.save()
    return True


@user_from_sid(Error404)
def bookkeeping(user, type_quantity):
    price = 0.0
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, "无权限操作")
    order = OrderInfo()
    order.uid_b=user
    order.o_state = order_state_choice.ACCEPTED
    order.save()
    for i in type_quantity:
        p_id = i.get("p_type")
        p_type = ProductSubType.objects.filter(id=p_id).first()
        if p_type is None:
            raise WLException(402, "品类不存在，清添加后操作")
        bpt = BusinessProductTypeBind.objects.filter(p_type=p_type).first()
        if bpt is None:
            raise WLException(403, "回收站对应的商品不存在，清添加后操作")
        if OrderProductType.objects.filter(p_type=p_type, oid=order).first():
            continue
        OrderProductType.objects.create(
            p_type=p_type,
            oid=order,
            quantity=i.get("quantity"),
            price=bpt.price
        )
        price_ = bpt.price * i.get("quantity")
        price += price_
    order.amount = price
    order.save()
    return order.id


@user_from_sid(Error404)
def bookkeeping_order_scan(user, oid, qr_info):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, "无权限操作")
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(407, "订单不存在")
    if order.o_state != order_state_choice.ACCEPTED:
        raise WLException(405, "该订单未被接单，不能执行此操作")
    user_id = caches["sessions"].get(qr_info)
    if user_id is None or user_id == '':
        raise WLException(402, "用户不存在，请重新获取二维码")
    try:
        user_c = UserBase.objects.get(id=user_id)
        c_delivery_info = UserDeliveryInfo.objects.filter(uid=user_c).first()
    except UserBase.DoesNotExist:
        raise WLException(403, "用户不存在或收获地址为空")
    order.uid_c = user_c
    order.c_delivery_info = c_delivery_info
    order.o_state = order_state_choice.COMPLETED
    order.save()
