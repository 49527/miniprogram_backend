# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _OrderStateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("创建"), "CREATED"),
        (1, _("已接单"), "ACCEPTED"),
        (2, _("被取消"), "CANCELED"),
        (3, _("已完成"), "COMPLETED"),
    )


order_state_choice = _OrderStateChoice()
