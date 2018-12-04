from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404
from usersys.choices.model_choice import user_validate_status
from usersys.models import UserBase, UserValidate
from ordersys.funcs.obtain import obtain_overview


@user_from_sid(Error404)
def obtain_self_info(user):
    # type: (UserBase) -> (UserBase, int)
    try:
        validate = user.user_validate
        is_validated = True if validate.validate_status == user_validate_status.ACCEPTED else False
    except UserValidate.DoesNotExist:
        is_validated = False
    n_times, total_amount = obtain_overview(user=user)
    return user, is_validated, n_times, total_amount
