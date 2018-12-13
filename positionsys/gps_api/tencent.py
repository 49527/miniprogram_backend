from django.conf import settings
import requests
from .base import GPSInterface


class TencentMap(GPSInterface):
    URL_DISTANCE = "https://apis.map.qq.com/ws/distance/v1/" \
                   "?mode=walking&from={lat_lng_s}&to={lat_lng_t}&key={key}"
    URL_ADDR2GPS = "https://apis.map.qq.com/ws/geocoder/v1/?address={address}&key={key}"
    URL_GPS2ADDR = "https://apis.map.qq.com/ws/geocoder/v1/?location={location}&key={key}"

    def __init__(self, key):
        self.key = key

    def _get_distance(self, from_, tos_):
        lat_lng_s = "{},{}".format(from_["lat"], from_["lng"])
        lat_lng_t = reduce(
            lambda to1, to2: "{};{}".format(to1, to2),
            map(
                lambda to: "{},{}".format(to["lat"], to["lng"]),
                tos_
            )
        )

        url = self.URL_DISTANCE.format(
            lat_lng_s=lat_lng_s, lat_lng_t=lat_lng_t, key=self.key
        )
        result = requests.get(url)
        re_dict = result.json()
        if re_dict["status"] != 0:
            raise ValueError(re_dict["message"])

        distances = [
            r["distance"] if r["distance"] >= 0 else None
            for r in re_dict["result"]["elements"]
        ]

        return distances

    def one_to_one_distance(self, from_, to_):
        return self._get_distance(from_, [to_])[0]

    def one_to_many_distance(self, from_, tos_):
        if len(tos_) == 0:
            return []

        return self._get_distance(from_, tos_)

    def resolve_address_to_gps(self, address):
        url = self.URL_ADDR2GPS.format(
            address=address, key=settings.MAP_KEY
        )

        result_dict = requests.get(url).json()
        if result_dict["status"] != 0:
            raise ValueError(result_dict["message"])

        return {
            "lat": result_dict["result"]["location"]["lat"],
            "lng": result_dict["result"]["location"]["lng"],
        }

    def resolve_gps_to_address(self, location):
        url = self.URL_GPS2ADDR.format(location="{},{}".format(location["lat"], location["lng"]), key=self.key)
        result = requests.get(url)
        result_dict = result.json()
        if result_dict["status"] != 0:
            raise ValueError(result_dict["message"])

        position_desc_dict = result_dict["result"]
        return position_desc_dict

