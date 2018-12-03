from business_sys.models import RecycleBin
from business_sys.choices.model_choices import recycle_bin_type
from django.conf import settings


def find_near_recycle_bin(lon, lat):
    l = settings.BOUND
    max_lon = lon + l
    min_lon = lon - l
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
