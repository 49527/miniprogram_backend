# coding=UTF-8
from base.util.field_choice import FieldChoice


class _DeliveryChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "NOT_EXIST"),
        (1, "", "EXIST"),

    )

is_delivery_exist = _DeliveryChoice()
