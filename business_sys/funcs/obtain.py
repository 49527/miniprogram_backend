# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from business_sys.models import BusinessProductTypeBind
from usersys.choices.model_choice import user_role_choice
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice


@user_from_sid(Error404)
def update_price(user, **data):
    type_price = data.get('type_price')
    for i in type_price:
        bpt = BusinessProductTypeBind.objects.filter(id=i.get('bpt_id')).first()
        if bpt is None:
            raise WLException(400, _("该记录不存在，操作失败"))
        if user.role == user_role_choice.CLIENT:
            raise WLException(401, _("您无权修改价格"))
        bpt.price = i.get('price')
        bpt.save()


@user_from_sid(Error404)
def get_category_list(user):
    category = ProductTopType.objects.filter(operator=top_type_choice.BUSINESS)
    return category