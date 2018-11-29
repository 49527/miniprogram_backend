# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _TransactionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("收款"), "COLLECT_MONEY"),
        (1, _("申请提现"), "APPLY"),
        (2, _("提现成功"), "GET_MONEY_SUCCESS"),
        (3, _("提现失败"), "GET_MONEY_FAILURE")
    )


transaction_type = _TransactionChoice()
