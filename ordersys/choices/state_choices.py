from base.util.field_choice import FieldChoice


class _OrderStateChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "CREATED"),
        (1, "", "ACCEPTED"),
        (2, "", "CANCELED"),
        (3, "", "COMPLETED"),
    )


order_state_choice = _OrderStateChoice()
