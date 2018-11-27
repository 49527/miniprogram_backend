from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from usersys.models import UserBase
from base.util.pages import get_page_info
from walletsys.models import Balance


@user_from_sid(Error404)
def obtain_balance(user):
    # type: (UserBase) -> QuerySet
    try:
        return user.balance.balance
    except Balance.DoesNotExist:
        return 0


@user_from_sid(Error404)
def obtain_history(user, page, count_per_page):
    # type: (UserBase, int, int) -> (QuerySet, int)
    qs = user.transaction
    start, end, n_pages = get_page_info(
        qs, count_per_page, page,
        index_error_excepiton=WLException(400, "Page out of range")
    )

    return qs.order_by("-id")[start:end], n_pages
