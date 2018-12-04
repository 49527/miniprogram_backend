from base.util.field_choice import FieldChoice


class _StateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "PN_NOT_BIND"),
        (1, "", "PN_BIND"),
    )


state_choice = _StateChoice()
