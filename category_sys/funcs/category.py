from category_sys.models import ProductTopType
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException


@user_from_sid(Error404)
def get_category_list(user):
    category = ProductTopType.objects.all()
    return category