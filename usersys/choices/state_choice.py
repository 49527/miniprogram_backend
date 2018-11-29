from base.util.field_choice import FieldChoice


class _StateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "PN_NOT_BIND"),
        (1, "", "PN_BIND"),
    )


class _ValidateStateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "NOT_VALIDATED"),
        (1, "", "VALIDATED"),
    )


state_choice = _StateChoice()
is_validate_choice = _ValidateStateChoice()
