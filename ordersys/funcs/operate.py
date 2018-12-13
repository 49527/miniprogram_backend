# coding=UTF-8
from __future__ import unicode_literals
import logging
import requests
from django.conf import settings
from django.utils.timezone import now
from django.core.cache import caches
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserDeliveryInfo, UserBase
from ordersys.models import OrderCancelReasonBind, OrderProductTypeBind, OrderInfo, OrderProductType
from ordersys.choices.model_choices import order_state_choice
from ordersys.funcs.utils import get_uncompleted_order_c
from category_sys.models import ProductSubType
from business_sys.models import BusinessProductTypeBind, RecyclingStaffInfo, RecycleBin
from usersys.choices.model_choice import user_role_choice


logger = logging.Logger(__name__)


def get_lng_lat(desc):
    url = "https://apis.map.qq.com/ws/geocoder/v1/?address={address}&key={key}".format(
        address=desc, key=settings.MAP_KEY
    )
    try:
        re = requests.get(url).json()["result"]
        print re
        lat_lng_desc = {
            "lat": re["location"]["lat"],
            "lng": re["location"]["lng"],
            "can_resolve_gps": True
        }
    except KeyError:
        return {
            "lat": None,
            "lng": None,
            "can_resolve_gps": False
        }
    return lat_lng_desc


@user_from_sid(Error404)
def submit_delivery_info(user, **data):
    data.update(get_lng_lat(data["address"]))
    return UserDeliveryInfo.objects.create(uid=user, **data)


@user_from_sid(Error404)
def cancel_order(user, order, reason=None, desc=None, **kwargs):

    if not order.uid_c == user:
        raise WLException(403, _("这个订单不属于该用户"))
    if order.o_state in (order_state_choice.CANCELED, order_state_choice.COMPLETED):
        raise WLException(403, _("此订单已完成或者已被取消，不能执行此操作"))
    if reason is None and desc is None:
        raise WLException(402, _("reason或者desc中至少有一个字段不能为空"))

    cancel_reason = OrderCancelReasonBind.objects.create(order=order, reason=reason, **kwargs)
    cancel_reason.desc = cancel_reason.reason.reason if desc is None else desc
    cancel_reason.save()
    order.o_state = order_state_choice.CANCELED
    order.save()


@user_from_sid(Error404)
def one_click_order(user, **data):
    if not get_uncompleted_order_c(user).count() == 0:
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
    if order.uid_b is not None:
        raise WLException(400, "订单已被抢")
    if OrderInfo.objects.filter(uid_b=user, o_state=order_state_choice.ACCEPTED).count() >= 3:
        raise WLException(406, "最多可以抢3单")
    o_state = order.o_state
    if o_state == order_state_choice.ACCEPTED:
        raise WLException(402, "已接单")
    if o_state == order_state_choice.CANCELED:
        raise WLException(403, "被取消")
    if o_state == order_state_choice.COMPLETED:
        raise WLException(405, "已完成")
    if order.o_state == order_state_choice.CREATED:
        order.uid_b = user
        order.o_state = order_state_choice.ACCEPTED
        order.grab_time = now()
        order.save()
    return order


@user_from_sid(Error404)
def cancel_order_b(user, order, reason, desc=None):

    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权限操作")
    try:
        order = OrderInfo.objects.get(id=order)
    except OrderInfo.DoesNotExist:
        raise WLException(407, u"订单不存在")
    if order.o_state in (order_state_choice.CANCELED, order_state_choice.COMPLETED):
        raise WLException(400, u"此订单已完成或者已被取消，不能执行此操作")
    if order.uid_b != user:
        raise WLException(402, u"这个订单不属于该用户,不能执行此操作")

    if order.can_cancel_b:
        order.o_state = order_state_choice.CANCELED
        order.save()
        cancel_bind, created = OrderCancelReasonBind.objects.get_or_create(
            order=order,
            defaults={
                "reason": reason,
                "desc": desc,
            }
        )
        if not created:
            logger.warn("A non-canceled order has a related cancel reason bind: %d - %d" % (order.id, cancel_bind.id))
            cancel_bind.reason = reason
            cancel_bind.desc = desc
            cancel_bind.save()

    else:
        raise WLException(403, u"您不能取消这个订单")


def check_type_quantity(type_quantity, recycle_bin):
    # type: (dict, RecycleBin) -> (list, float)
    amount = 0.0
    list_product_types = []
    category_ids = [sub_type["p_type"] for sub_type in type_quantity]
    p_type_queryset_dict = dict(
        map(lambda x: (x.id, x), list(ProductSubType.objects.filter(id__in=category_ids)))
    )
    if len(p_type_queryset_dict) != len(type_quantity):
        raise WLException(401, u"品类不存在，清添加后操作")

    bpt_queryset = BusinessProductTypeBind.objects.select_related('p_type').filter(
        p_type_id__in=category_ids, recycle_bin=recycle_bin
    )
    bpt_queryset_dict = dict(
        map(lambda x: (x.p_type.id, x), list(bpt_queryset))
    )
    if len(bpt_queryset_dict) != len(type_quantity):
        raise WLException(401, u"品类不存在，清添加后操作")

    for sub_type_price in type_quantity:
        p_id = sub_type_price["p_type"]

        if sub_type_price.get("quantity", 0) == 0:
            continue

        price = bpt_queryset_dict[p_id].price * sub_type_price.get("quantity")
        list_product_types.append({
            "p_type": p_type_queryset_dict[p_id],
            "quantity": sub_type_price.get("quantity"),
            "price": price
        })
        amount += price

    if amount == 0:
        raise WLException(403, u"记账总额为不能为0.")

    return list_product_types, amount


@user_from_sid(Error404)
def bookkeeping_order(user, oid, type_quantity):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权限操作")

    try:
        recycle_bin = RecyclingStaffInfo.objects.get(uid=user).recycle_bin
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(402, u"还没有绑定回收站")

    list_product_types, amount = check_type_quantity(type_quantity, recycle_bin)

    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(407, u"订单不存在")

    order.amount = amount
    order.o_state = order_state_choice.COMPLETED
    order.complete_time = now()
    order.recycle_bin = recycle_bin
    order.save()

    for product_type in list_product_types:
        OrderProductType.objects.create(oid=order, **product_type)


@user_from_sid(Error404)
def bookkeeping_order_pn(user, pn, type_quantity):
    # type: (UserBase, str, dict) -> None

    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权限操作")

    try:
        recycle_bin = RecyclingStaffInfo.objects.get(uid=user).recycle_bin
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(402, u"还没有绑定回收站")

    list_product_types, amount = check_type_quantity(type_quantity, recycle_bin)

    order = OrderInfo.objects.create(
        uid_b=user,
        o_state=order_state_choice.COMPLETED,
        complete_time=now(),
        grab_time=now(),
        recycle_bin=recycle_bin,
        pn=pn,
        amount=amount
    )

    for product_type in list_product_types:
        OrderProductType.objects.create(oid=order, **product_type)


@user_from_sid(Error404)
def bookkeeping_order_scan(user, qr_info, type_quantity):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权限操作")

    user_c_id = caches["sessions"].get(qr_info)
    if user_c_id is None:
        raise WLException(406, u"二维码已过期，请重新获取")

    try:
        user_c = UserBase.objects.get(id=user_c_id)
    except UserBase.DoesNotExist:
        raise WLException(405, u"获取客户信息失败")

    try:
        recycle_bin = RecyclingStaffInfo.objects.get(uid=user).recycle_bin
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(402, u"还没有绑定回收站")

    list_product_types, amount = check_type_quantity(type_quantity, recycle_bin)

    order = OrderInfo.objects.create(
        uid_b=user,
        uid_c=user_c,
        o_state=order_state_choice.COMPLETED,
        grab_time=now(),
        complete_time=now(),
        recycle_bin=recycle_bin,
        amount=amount
    )

    for product_type in list_product_types:
        OrderProductType.objects.create(oid=order, **product_type)
