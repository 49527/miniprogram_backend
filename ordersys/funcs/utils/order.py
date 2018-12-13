from django.db.models import Q
from ordersys.models import OrderInfo
from ordersys.choices.model_choices import order_state_choice
from usersys.models import UserBase


def get_uncompleted_order_c(user):
    # type: (UserBase) -> (Queryset)
    return user.order_c.filter(
        Q(o_state=order_state_choice.CREATED) | Q(o_state=order_state_choice.ACCEPTED)
    )


def get_completed_order(**kwargs):
    qs = OrderInfo.objects.filter(
        o_state=order_state_choice.COMPLETED,
    )
    if len(kwargs) > 0:
        qs = qs.filter(**kwargs)

    return qs


def get_uncompleted_order(**kwargs):
    qs = OrderInfo.objects.filter(
        Q(o_state=order_state_choice.CREATED) | Q(o_state=order_state_choice.ACCEPTED),
    )
    if len(kwargs) > 0:
        qs = qs.filter(**kwargs)

    return qs
