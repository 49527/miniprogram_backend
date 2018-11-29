# coding=UTF-8
from django.utils.translation import ugettext_lazy as _
from base.util.field_choice import FieldChoice


class _ValidateStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, _("用户尚未提交认证审核申请"), "NOT_COMMITTED"),
        (1, _("用户已提交认证审核申请，但审核尚未被处理"), "NOT_PROCEEDED"),
        (2, _("用户已提交认证审核申请，且审核已通过"), "ACCEPTED"),
        (3, _("用户已提交认证审核申请，但审核被拒绝"), "REJECTED"),
    )


user_validate_status = _ValidateStatusChoice()
