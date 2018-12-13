# coding=utf-8
from django.db import models
from django.db import transaction
from django.utils.timezone import now
from base.exceptions import Error404, WLException
from base.util.none_to_0 import none_to_0
from usersys.models import UserBase
from usersys.funcs.utils.usersid import user_from_sid
from business_sys.models import (
    Truck,
    LoadingCredential,
    LoadingCredentialDetail,
    RecyclingStaffInfo,
)
from ordersys.funcs.utils import get_completed_order
from usersys.choices.model_choice import user_role_choice


def get_quantity_price(user):
    qs = get_completed_order(
        uid_b=user, loaded=False
    )

    summary = qs.values("order_detail_b__p_type__unit").annotate(
        price=models.Sum("order_detail_b__price"),
        quantity=models.Sum("order_detail_b__quantity"),
        create_time=models.Min("create_time"),
    )

    quantity_by_unit = []
    total_price = 0
    unloaded_start_time = now()
    for s in summary:
        quantity_by_unit.append({
            "unit": s["order_detail_b__p_type__unit"],
            "quantity": none_to_0(s["quantity"]),
            "price": none_to_0(s["price"])
        })

        total_price += none_to_0(s["price"])
        unloaded_start_time = min(unloaded_start_time, s["create_time"])

    return quantity_by_unit, total_price, unloaded_start_time


@user_from_sid(Error404)
def get_truck_info(user):
    # type: (UserBase) -> dict
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权访问")

    quantity, price, unloaded_start_time = get_quantity_price(user)

    return {
        "end_time": unloaded_start_time,
        "time_diff": (now() - unloaded_start_time).total_seconds(),
        "price": price,
        "quantity": quantity
    }


@user_from_sid(Error404)
def create_truck_info(user, number_plate):
    # type: (UserBase, unicode) -> LoadingCredential
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权访问")

    try:
        recycle_bin = user.recycling_staff_info.recycle_bin
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(401, u"用户未绑定回收站")

    number_plate_formatted = number_plate.replace(u" ", u"").upper()

    # FIXME: Everyone can create a truck now.
    truck, created = Truck.objects.get_or_create(number_plate=number_plate_formatted)

    with transaction.atomic():
        lc = LoadingCredential.objects.create(
            uid_b=user,
            recycle_bin=recycle_bin,
            truck=truck,
        )

        related_order = get_completed_order(uid_b=user, loaded=False)
        related_order.update(loaded=True, loading_cred=lc)

        combined = related_order.values(
            category=models.F("order_detail_b__p_type")
        ).annotate(
            quantity=models.Sum("order_detail_b__quantity"),
            price=models.Sum("order_detail_b__price"),
        )

        for c in combined:
            LoadingCredentialDetail.objects.create(
                credential=lc,
                **c
            )

    return lc
