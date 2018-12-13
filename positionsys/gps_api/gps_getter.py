from django.conf import settings
from django.utils.module_loading import import_string


gps_getter = import_string(settings.GPS_GETTER["class"])(**settings.GPS_GETTER.get("kwargs", {}))
