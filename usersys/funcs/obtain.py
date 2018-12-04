from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404
from usersys.choices.state_choice import is_validate_choice
from usersys.choices.model_choice import user_validate_status
from usersys.models import UserBase, UserValidate
from django.core.cache import caches
import uuid


@user_from_sid(Error404)
def obtain_self_info(user):
    # type: (UserBase) -> (UserBase, int)
    try:
        validate = user.user_validate
        state = is_validate_choice.VALIDATED if validate.validate_status == user_validate_status.ACCEPTED \
            else is_validate_choice.NOT_VALIDATED
    except UserValidate.DoesNotExist:
        state = is_validate_choice.NOT_VALIDATED
    return user, state


@user_from_sid(Error404)
def obtain_qr_info(user):
    # type: (UserBase) -> str
    qr_info = str(uuid.uuid1())
    caches["sessions"].set(qr_info, user.id, 300)
    return qr_info
