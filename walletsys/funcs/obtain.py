from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import *
from usersys.models import UserBase
from base.util.pages import get_page_info


@user_from_sid(Error404)
def obtain_balance(user):
    return user.Balance.last().balance


@user_from_sid(Error404)
def obtain_history(user, page, count_per_page):
    # type: (UserBase, int, int) -> QuerySet
    qs = user.Transaction_Detail
    start, end, n_pages = get_page_info(qs, count_per_page, page,
                                        index_error_excepiton=WLException(400, "Page out of range"))

    return qs.order_by("-id")[start:end], n_pages
