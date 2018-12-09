# coding=utf-8
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.choices.model_choice import user_role_choice
from usersys.models import UserBase
from business_sys.models import RecyclingStaffInfo
from ordersys.funcs.obtain import obtain_overview


@user_from_sid(Error404)
def obtain_self_info_b(user):
    # type: (UserBase) -> (int, int)
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, u"无权访问")

    try:
        recycle_bin = user.recycling_staff_info.recycle_bin
    except RecyclingStaffInfo.DoesNotExist:
        raise WLException(402, u"该用户信息尚未完善")

    n_times, total_amount = obtain_overview(user=user)
    return {
        "pn": user.pn,
        "total_amount": total_amount,
        "recycle_bin": recycle_bin,
    }
