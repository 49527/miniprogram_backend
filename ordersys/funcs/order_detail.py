# coding=utf-8
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.choices.model_choice import user_role_choice
from usersys.models import UserBase
from django.db import models
from ordersys.choices.model_choices import order_state_choice
from ordersys.models import OrderInfo, OrderProductType


@user_from_sid(Error404)
def get_order_detail(user, oid):
    # type: (UserBase, OrderInfo) -> QuerySet
    if oid.uid_b != user and oid.uid_c != user:
        raise WLException(401, u"无权获取订单信息")

    if oid.o_state != order_state_choice.COMPLETED:
        raise WLException(401, u"订单未完成")

    return oid.order_detail_b.all()


@user_from_sid(Error404)
def get_orders_summary_c(user):
    # type: (UserBase) -> QuerySet
    if user.role != user_role_choice.CLIENT:
        raise WLException(401, u"无权调用该接口")

    return OrderProductType.objects.select_related("oid").filter(
        oid__o_state=order_state_choice.COMPLETED,
        oid__uid_c=user,
    ).values("p_type__toptype_c", "p_type__toptype_c__t_top_name").annotate(
        price=models.Sum(models.F("price") * models.F("quantity")),
        quantity=models.Sum("quantity")
    )
