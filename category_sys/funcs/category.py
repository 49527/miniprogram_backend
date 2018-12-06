from category_sys.models import ProductTopType
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from category_sys.choices.model_choices import top_type_choice


@user_from_sid(Error404)
def get_category_list(user):
    category = ProductTopType.objects.filter(operator=top_type_choice.BUSINESS)
    return category
