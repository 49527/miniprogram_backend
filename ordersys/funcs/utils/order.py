from django.db.models import Q
from ordersys.choices.model_choices import order_state_choice
from usersys.models import UserBase


def get_uncompleted_order(user):
    # type: (UserBase) -> (Queryset)
    return user.order_c.filter(
        Q(o_state=order_state_choice.CREATED) | Q(o_state=order_state_choice.ACCEPTED)
    )
