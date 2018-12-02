from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserDeliveryInfo
from ordersys.models import OrderReasonBind, OrderProductTypeBind, OrderInfo
from ordersys.choices.model_choices import order_state_choice
from django.db.models import Q

@user_from_sid(Error404)
def submit_delivery_info(user, **data):
    UserDeliveryInfo.objects.create(uid=user,**data)


@user_from_sid(Error404)
def cancel_order(user, **data):
    order = data["order"]

    if not order.uid_c == user:
        raise WLException(403, "this order is not belong to this user")
    if order.o_state == order_state_choice.CANCELED or order.o_state == order_state_choice.COMPLETED:
        raise  WLException(403, "order in this state cannot be canceled")
    if data.get("reason", None) is None and data.get("desc", None) is None:
        raise WLException(402, "reason or desc should be filled")

    OrderReasonBind.objects.create(**data)
    order.o_state = order_state_choice.CANCELED
    order.save()


@user_from_sid(Error404)
def one_click_order(user, contact_pn, type_quantity):
    if not user.order_c.filter(
        Q(o_state=order_state_choice.CREATED) | Q(o_state=order_state_choice.ACCEPTED)
    ).count() == 0:
        raise WLException(403, "there exist a order uncompleted")
    order = OrderInfo.objects.create(uid_c=user, contact_pn_c=contact_pn, o_state=order_state_choice.CREATED)
    for dic in type_quantity:
        OrderProductTypeBind.objects.create(oid=order, **dic)
