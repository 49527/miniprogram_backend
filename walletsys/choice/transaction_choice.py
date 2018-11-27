from base.util.field_choice import FieldChoice


class _TransactionChoice(FieldChoice):
    CHOICE_DISPLAY = (
        (0, "", "COLLECT_MONEY"),
        (1, "", "APPLY"),
        (2, "", "GET_MONEY_SUCCESS"),
        (3, "", "GET_MONEY_FAILURE")
    )

transaction_type = _TransactionChoice()
