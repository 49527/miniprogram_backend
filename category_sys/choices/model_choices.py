# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _TopTypeChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("C端类型"), "CONSUMER"),
        (1, _("B端类型"), "BUSINESS"),
    )


class _TypeUnitChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("个"), "PIECE"),
        (1, _("斤"), "CATTY")
    )


top_type_choice = _TopTypeChoice()
type_unit_choice = _TypeUnitChoice()
