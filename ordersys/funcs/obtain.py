from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserBase, UserDeliveryInfo
from base.util.pages import get_page_info
from django.db import models
from ordersys.choices.model_choices import order_state_choice
from ordersys.models import OrderCancelReason
from business_sys.models import RecycleBin
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice

@user_from_sid(Error404)
def obtain_order_list(user, page, count_per_page):
    # type: (UserBase, int, int) -> (QuerySet, int)
    qs = user.order
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages


@user_from_sid(Error404)
def obtain_overview(user):
    # type: (UserBase) -> (int, float)
    orders = user.order
    n_times = orders.count()
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
    uncompleted = user.order_c.filter(
        models.Q(o_state=order_state_choice.CREATED) | models.Q(o_state=order_state_choice.ACCEPTED)
    )
    return uncompleted.order_by('id').last(), uncompleted.count()


@user_from_sid(Error404)
def obtain_c_toptype_list(user):
    type_list = []
    qs = RecycleBin.objects.all()
    for c_type in ProductTopType.objects.filter(operator=top_type_choice.CONSUMER):
        dic = {
            "type_id": c_type.id,
            "c_type": c_type.t_top_name,
            "min_price": qs.filter(product_subtype__p_type__sub2top__top_type=c_type).aggregate(
                models.Min("product_subtype__price"))["product_subtype__price__min"],
            "max_price": qs.filter(product_subtype__p_type__sub2top__top_type=c_type).aggregate(
                models.Max("product_subtype__price"))["product_subtype__price__max"]
        }
        type_list.append(dic)

    return type_list


@user_from_sid(Error404)
def obtain_cancel_reason(user):
    return OrderCancelReason.objects.filter(in_use=True)
