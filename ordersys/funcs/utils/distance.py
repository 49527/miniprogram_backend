import logging
from positionsys import gps_getter
from ordersys.models import OrderInfo


logger = logging.getLogger(__name__)


def append_distance_for_orders(orders, lat, lng, many=False):

    def has_gps(o_list):
        o_e = o_list  # type: OrderInfo
        if o_e.c_delivery_info is None:
            return False

        return o_e.c_delivery_info.can_resolve_gps

    if not many:
        order_list = [orders]
    else:
        order_list = list(orders)  # type: list

    # preprocess distance attribute
    for o in order_list:
        o.distance = None

    orders_has_gps = filter(has_gps, order_list)

    lan_lat_list_to_calc = map(lambda o_e: {
        "lat": o_e.c_delivery_info.lat,
        "lng": o_e.c_delivery_info.lng,
    }, orders_has_gps)

    source = {
        "lat": lat,
        "lng": lng,
    }

    try:
        distances = gps_getter.one_to_many_distance(source, lan_lat_list_to_calc)
    except ValueError as e:
        logger.warn("gps_getter {} failed to get distances, message: {}".format(repr(gps_getter), e.message))
        return

    for distance, order_has_gps in zip(distances, orders_has_gps):
        order_has_gps.distance = distance
