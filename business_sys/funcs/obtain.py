from business_sys.funcs.utils.near import find_near_recycle_bin, get_one_to_many_distance, get_one_to_one_distance
from business_sys.models import RecycleBin


def obtain_nearby_recycle_bin(lng, lat):
    r_b_qs = find_near_recycle_bin(lng, lat)
    lon_lat_qs = r_b_qs.values('GPS_L', 'GPS_A')
    closest = get_one_to_many_distance(lng, lat, lon_lat_qs)
    query_list = []
    while not len(closest) == 0:
        position = closest.pop(0)
        qs = r_b_qs.get(GPS_L=position["lng"], GPS_A=position["lat"])
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
    return rb, distance
