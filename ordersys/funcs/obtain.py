# coding=utf-8
import datetime
from pytz import timezone
from dateutil import relativedelta
from django.utils.timezone import now
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
from django.utils.translation import ugettext_lazy as _
from business_sys.funcs.utils.positon import get_one_to_one_distance
from django.core.cache import caches


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
    qs = get_user_order_queryset(user).filter(o_state=order_state_choice.COMPLETED)
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages, qs.count()


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
    pn = user.pn
    if user_delivery.count() == 0:
        exist = False
    else:
        exist = True
    return user_delivery.order_by('id').last(), exist, pn


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


@user_from_sid(Error404)
def obtain_order_detail(user, oid):
    # type: (UserBase, int) -> (OrderInfo)
    order = OrderInfo.objects.get(id=oid)
    if not order.uid_c == user:
        raise WLException(403, _("没有权限查看该订单"))
    return order


def obtain_c_toptype_list():
    type_list = []
    qs = RecycleBin.objects.all()
    for c_type in ProductTopType.objects.filter(operator=top_type_choice.CONSUMER, in_use=True):
        try:
            unit = c_type.c_subtype.filter(in_use=True).first().unit
        except AttributeError:
            unit = None
        dic = {
            "type_id": c_type.id,
            "c_type": c_type.t_top_name,
            "unit" : unit,
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


def obtain_order_list_by_o_state(page, count_per_page):
    # type: (int, int) -> (QuerySet, int)
    qs = OrderInfo.objects.filter(o_state=order_state_choice.CREATED)
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )
    count = qs.count()
    return qs.order_by("-id")[start:end], n_pages, count


@user_from_sid(Error404)
def obtain_order_details(user, oid):
    # type: (UserBase, int) -> (OrderProductType, int)
    try:
        order = OrderInfo.objects.get(id=oid)
    except OrderInfo.DoesNotExist:
        raise WLException(404, u"订单不存在")
    if order.uid_b != user:
        raise WLException(404, u"订单不存在")

    if order.c_delivery_info.can_resolve_gps:
        lat_c = order.c_delivery_info.lat
        lng_c = order.c_delivery_info.lng
        user_b_gps = caches["sessions"].get("user_b_gps")
        lat_b = user_b_gps['lat']
        lng_b = user_b_gps['lng']
        distance = get_one_to_one_distance(lat_b, lng_b, lat_c, lng_c)
    else:
        distance = None

    return order, distance


@user_from_sid(Error404)
def obtain_order_list_b(user, start_date, end_date, page, count_per_page):
    # type: (UserBase, datetime, datetime, int, int) -> (QuerySet, int)
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权操作")
    qs = OrderInfo.objects.filter(create_time__gte=start_date, create_time__lte=end_date)
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages


def get_datetime(t):
    # get start and end of this week
    week_s = t + relativedelta.relativedelta(hour=0, minute=0, second=0, weekday=relativedelta.MO(-1))
    week_e = t + relativedelta.relativedelta(hour=23, minute=59, second=59, weekday=relativedelta.SU(0))
    month_s = t + relativedelta.relativedelta(hour=0, minute=0, second=0, day=1)
    month_e = t + relativedelta.relativedelta(hour=23, minute=59, second=59, day=1, months=1, days=-1)
    day_s = t + relativedelta.relativedelta(hour=0, minute=0, second=0)
    day_e = t + relativedelta.relativedelta(hour=23, minute=59, second=59)
    return week_s, week_e, month_s, month_e, day_s, day_e


@user_from_sid(Error404)
def obtain_order_count(user):
    def none_to_zero(obj):
        return obj if obj is not None else 0

    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权操作")
    t_now = now().astimezone(timezone(settings.TIME_ZONE))
    week_s, week_e, month_s, month_e, day_s, day_e = get_datetime(t_now)
    qs = OrderProductType.objects.filter(oid__o_state=order_state_choice.COMPLETED, oid__uid_b=user)

    all_ = qs.aggregate(models.Sum('quantity'), models.Sum('price'))

    month_ = qs.filter(
        oid__create_time__gte=month_s,
        oid__create_time__lte=month_e
    ).aggregate(models.Sum('quantity'), models.Sum('price'))

    week_ = qs.filter(
        oid__create_time__gte=week_s,
        oid__create_time__lte=week_e
    ).aggregate(models.Sum('quantity'), models.Sum('price'))

    day_ = qs.filter(
        oid__create_time__gte=day_s,
        oid__create_time__lte=day_e
    ).aggregate(models.Sum('quantity'), models.Sum('price'))

    data = {
        "month": {"quantity": month_["quantity__sum"], "price": month_["price__sum"]},
        "week": {"quantity": week_["quantity__sum"], "price": week_["price__sum"]},
        "day": {"quantity": day_["quantity__sum"], "price": day_["price__sum"]},
        "all": {"quantity": all_["quantity__sum"], "price": all_["price__sum"]},
    }

    # make all null values to 0
    data = {
        k: {
            k_inner: none_to_zero(v_inner) for k_inner, v_inner in v.iteritems()
        } for k, v in data.iteritems()}
    return data
