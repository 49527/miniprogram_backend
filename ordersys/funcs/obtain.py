# coding=utf-8
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.choices.model_choice import user_role_choice
from usersys.models import UserBase, UserDeliveryInfo
from base.util.pages import get_page_info
from django.db import models
from ordersys.choices.model_choices import order_state_choice
from ordersys.models import OrderCancelReason, OrderInfo, OrderProductType, OrderReasonBind
from business_sys.models import RecycleBin
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice
from ordersys.funcs.utils import get_uncompleted_order
from django.utils.timezone import now
from django.conf import settings


def get_user_order_queryset(user):
    if user.role == user_role_choice.CLIENT:
        qs = user.order_c
    elif user.role == user_role_choice.RECYCLING_STAFF:
        qs = user.order_b
    else:
        raise AssertionError("user's role is neither CLIENT nor RECYCLER")

    return qs


@user_from_sid(Error404)
def obtain_order_list(user, page, count_per_page):
    # type: (UserBase, int, int) -> (QuerySet, int)
    qs = get_user_order_queryset(user)
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages


@user_from_sid(Error404)
def obtain_overview(user):
    # type: (UserBase) -> (int, float)
    orders = get_user_order_queryset(user)
    n_times = orders.filter(o_state=order_state_choice.COMPLETED).count()
    total_amount = orders.filter(o_state=order_state_choice.COMPLETED).aggregate(models.Sum('amount'))["amount__sum"]
    total_amount = 0 if total_amount is None else total_amount
    return n_times, total_amount


@user_from_sid(Error404)
def obtain_delivery_info(user):
    # type: (UserBase) -> (UserDeliveryInfo, int)
    user_delivery = user.user_delivery_info.filter(in_use=True)
    if user_delivery.count() == 0:
        exist = False
    else:
        exist = True
    return user_delivery.order_by('id').last(), exist


@user_from_sid(Error404)
def obtain_uncompleted(user):
    # type: (UserBase) -> (UserDeliveryInfo, int)
    uncompleted = get_uncompleted_order(user)
    if uncompleted.count() == 0:
        order = None
        exist = False
    else:
        exist = True
        order = uncompleted.order_by('id').last()
        if (now() - order.create_time).total_seconds() > settings.TIME_FOR_SET_ORDER \
                and order.o_state == order_state_choice.CREATED:
            order.o_state = order_state_choice.CANCELED
            order.save()
            OrderReasonBind.objects.create(desc=u'订单超时', order=order)

    return order, exist


def obtain_c_toptype_list():
    type_list = []
    qs = RecycleBin.objects.all()
    for c_type in ProductTopType.objects.filter(operator=top_type_choice.CONSUMER, in_use=True):
        dic = {
            "type_id": c_type.id,
            "c_type": c_type.t_top_name,
            "min_price": qs.filter(product_subtype__p_type__toptype_c=c_type,
                                   product_subtype__p_type__in_use=True).aggregate(
                models.Min("product_subtype__price"))["product_subtype__price__min"],
            "max_price": qs.filter(product_subtype__p_type__toptype_c=c_type,
                                   product_subtype__p_type__in_use=True).aggregate(
                models.Max("product_subtype__price"))["product_subtype__price__max"]
        }
        type_list.append(dic)
    modified_time = qs.filter(product_subtype__p_type__in_use=True).aggregate(
        models.Max("product_subtype__modified_time"))["product_subtype__modified_time__max"]

    return type_list, modified_time


def obtain_cancel_reason():
    return OrderCancelReason.objects.filter(in_use=True)


# @user_from_sid(Error404)
def obtain_order_list_by_o_state(page, count_per_page):
    # type: (int, int) -> (QuerySet, int)
    qs = OrderInfo.objects.filter(o_state=order_state_choice.CREATED)
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages


@user_from_sid(Error404)
def obtain_order_details(user, oid):
    # type: (UserBase, int) -> OrderProductType
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(404, u"订单不存在")
    if order.uid_b != user:
        raise WLException(404, u"订单不存在")
    order_product = OrderProductType.objects.filter(oid=order)
    return order_product, order
