from business_sys.models import RecycleBin
from business_sys.choices.model_choices import recycle_bin_type
from django.conf import settings
import requests
from operator import itemgetter


def find_near_recycle_bin(lng, lat):
    l = settings.BOUND
    max_lon = lng + l
    min_lon = lng - l
    max_lat = lat + l
    min_lat = lat - l
    qs = RecycleBin.objects.filter(
        r_b_type=recycle_bin_type.FIXED,
        GPS_L__gte=min_lon,
        GPS_L__lte=max_lon,
        GPS_A__gte=min_lat,
        GPS_A__lte=max_lat
    )
    return qs


def get_one_to_many_distance(lng, lat, lon_lat_list):

    num = min(settings.NUM_OF_NEAR_BIN, len(lon_lat_list))
    id_list = [l["id"] for l in lon_lat_list]

    if len(lon_lat_list) == 0:
        return []
    else:
        lat_lon = reduce(lambda a, b: a + ";" + b,
                         [str(item["GPS_A"]) + ',' + str(item["GPS_L"]) for item in lon_lat_list])

    url = "https://apis.map.qq.com/ws/distance/v1/" \
          "?mode=walking&from={lat},{lng}&to={lat_lon}&key={key}".format(
        lng=lng, lat=lat, lat_lon=lat_lon, key=settings.MAP_KEY
    )
    re = requests.get(url)
    elements = re.json()["result"]["elements"]
    position = [
        dict(
            {
                "distance": e["distance"],
                "id": rid,
            },
            **e["to"]
        ) for e, rid in zip(elements, id_list)
    ]
    position = sorted(position, key=itemgetter("distance"))
    return position[0: num]


def get_one_to_one_distance(lng, lat, GPS_L, GPS_A):
    lat_lon = str(GPS_A) + ',' + str(GPS_L)
    url = "https://apis.map.qq.com/ws/distance/v1/" \
          "?mode=walking&from={lat},{lng}&to={lat_lon}&key={key}".format(
        lng=lng, lat=lat, lat_lon=lat_lon, key=settings.MAP_KEY
    )
    re = requests.get(url)
    return re.json()["result"]["elements"][0]["distance"]
