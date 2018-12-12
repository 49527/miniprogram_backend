

class GPSInterface(object):
    def one_to_one_distance(self, from_, to_):
        # type: (dict, dict) -> float
        """
        Get distance from source to destination gps positions.
        :param from_: a dictionary containing lat and lng key with string or float value
                      example: {"lat": "11.11111", "lng": "22.22222"}
        :param to_: a dictionary containing lat and lng key with string or float value
                    example: {"lat": "11.11111", "lng": "22.22222"}
        :return: a float value indicates the distance
        """
        raise NotImplementedError

    def one_to_many_distance(self, from_, tos_):
        # type: (dict, dict) -> list
        """
        Get distance from source to a list of destination gps positions.
        :param from_: a dictionary contains lat and lng key with string or float value
                      example: {"lat": "11.11111", "lng": "22.22222"}
        :param tos_: a list of dictionaries containing lat and lng key with string or float value
                    example: [{"lat": "11.11111", "lng": "22.22222"}, ...]
        :return: a list of float value indicates the distances
        """
        raise NotImplementedError

    def resolve_address_to_gps(self, address):
        # type: (str) -> dict
        """
        Resolve the gps of an address.
        :param address: a string indicates the address.
        :return: a dictionary containing lat and lng key.
        """
        raise NotImplementedError

    def resolve_gps_to_address(self, location):
        # type: (dict) -> dict
        """
        Resolve the address of a gps location.
        :param location: a dictionary containing lat and lng key.
        :return: a dictionary of the description of the location. Maybe different among map api.
        """
        raise NotImplementedError
