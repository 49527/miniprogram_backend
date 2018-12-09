# coding=utf-8
import uuid
from django.core.cache import caches
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.choices.model_choice import user_validate_status, user_role_choice
from usersys.models import UserBase, UserValidate
from ordersys.funcs.obtain import obtain_overview
from .utils.qr import qr_format


@user_from_sid(Error404)
def obtain_self_info(user):
    # type: (UserBase) -> (UserBase, bool, int, float)
    try:
        validate = user.user_validate
        is_validated = True if validate.validate_status == user_validate_status.ACCEPTED else False
    except UserValidate.DoesNotExist:
        is_validated = False
    n_times, total_amount = obtain_overview(user=user)
    return user, is_validated, n_times, total_amount


@user_from_sid(Error404)
def obtain_qr_info(user):
    # type: (UserBase) -> str
    qr_info = qr_format(str(uuid.uuid1()))
    caches["sessions"].set(qr_info, user.id, 300)
    return qr_info
