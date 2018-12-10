# coding=utf-8
import datetime
from django.db import models
from django.conf import settings
from pytz import timezone
from base.exceptions import Error404, WLException
from usersys.funcs.utils.usersid import user_from_sid
from business_sys.models.truck import Truck, TruckUserBind
from ordersys.models.order import OrderProductType
from ordersys.choices.model_choices import order_state_choice
from usersys.choices.model_choice import user_role_choice


def get_quantity_price(user):
    t_now = datetime.datetime.now().replace(tzinfo=timezone(settings.TIME_ZONE))
    end_time = TruckUserBind.objects.filter(uid_b=user).aggregate(models.Max("truck__end_time"))["truck__end_time__max"]
    qs = OrderProductType.objects.filter(oid__o_state=order_state_choice.COMPLETED, oid__uid_b=user)
    if end_time is None:
        end_time = '2018-12-10 00:00:00'
    opt = qs.filter(
        oid__create_time__gte=end_time,
        oid__create_time__lte=t_now
    ).aggregate(models.Sum('quantity'), models.Sum('price'))
    quantity = opt["quantity__sum"] if opt["quantity__sum"] is not None else 0.0
    price = opt["price__sum"] if opt["price__sum"] is not None else 0.0
    return quantity, price, end_time, t_now


@user_from_sid(Error404)
def get_truck_info(user):
    # type: (TruckUserBind) -> (dict)
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权访问")

    quantity, price, end_time, t_now = get_quantity_price(user)

    return {"end_time": end_time,
            "time_diff": end_time-t_now,
            "price": price,
            "quantity": quantity}


@user_from_sid(Error404)
def create_truck_info(user, number_plate):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权访问")

    quantity, price, end_time, t_now = get_quantity_price(user)

    truck = Truck.objects.create(
        number_plate=number_plate,
        amount=price,
        start_time=end_time,
        quantity=quantity
    )

    TruckUserBind.objects.create(
        uid_b=user,
        truck=truck
    )