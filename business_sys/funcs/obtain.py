# coding=utf-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from usersys.funcs.utils.usersid import user_from_sid
from base.exceptions import Error404, WLException
from business_sys.models import BusinessProductTypeBind, RecyclingStaffInfo, RecycleBin
from usersys.choices.model_choice import user_role_choice
from category_sys.models import ProductTopType
from category_sys.choices.model_choices import top_type_choice
from business_sys.funcs.utils.positon import find_near_recycle_bin, get_one_to_many_distance, get_one_to_one_distance,\
    get_position_desc


def obtain_nearby_recycle_bin(lng, lat):
    r_b_qs = find_near_recycle_bin(lng, lat)
    lon_lat_qs = r_b_qs.values('GPS_L', 'GPS_A', 'id')
    closest = get_one_to_many_distance(lng, lat, lon_lat_qs)
    query_list = []
    while not len(closest) == 0:
        position = closest.pop(0)
        qs = r_b_qs.get(id=position["id"])
        query_list.append({"recycle_bin": qs, "distance": position["distance"]})
    return query_list


def obtain_recycle_bin_detail(lng, lat, rb_id):
    rb = RecycleBin.objects.get(id=rb_id)

    distance = get_one_to_one_distance(
        lng=lng,
        lat=lat,
        GPS_A=rb.GPS_A,
        GPS_L=rb.GPS_L
    )
    position_desc = get_position_desc(lng=lng, lat=lat)
    return rb, distance, position_desc


@user_from_sid(Error404)
def update_price(user, type_price):
    if user.role != user_role_choice.RECYCLING_STAFF:
        raise WLException(401, _("您无权修改价格"))
    rsi = RecyclingStaffInfo.objects.filter(uid=user).first()
    if rsi is None:
        raise WLException(401, _("您无权修改价格"))
    recycle_bin = rsi.recycle_bin
    for i in type_price:
        bpt = BusinessProductTypeBind.objects.filter(p_type__id=i.get('pst_id')).first()
        if bpt is None:
            raise WLException(400, _("该记录不存在，操作失败"))
        if bpt.recycle_bin != recycle_bin:
            raise WLException(401, _("您无权修改价格"))
        bpt.price = i.get('price')
        bpt.save()


def get_category_list():
    category = ProductTopType.objects.filter(operator=top_type_choice.BUSINESS)
    return category
