# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _RecycleBinTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("固定站"), "FIXED"),
        (1, _("流动站"), "FLOW"),
    )


class _BusinessStaffBindStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("默认状态"), "DEFAULT"),
    )


recycle_bin_type = _RecycleBinTypeChoice()
business_staff_status = _BusinessStaffBindStatusChoice()
