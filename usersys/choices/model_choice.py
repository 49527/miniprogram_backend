# coding=UTF-8
from base.util.field_choice import FieldChoice


class _ValidateStatusChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "NOT_COMMITTED"),
        (1, "", "NOT_PROCEEDED"),
        (2, "", "ACCEPTED"),
        (3, "", "REJECTED"),
    )


user_validate_status = _ValidateStatusChoice()
