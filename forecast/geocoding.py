#  MIT License
#
#  Copyright (c) 2023 Ian Buttimer
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
import json
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import re
import googlemaps
from datetime import datetime

from django.conf import settings

from utils import dict_drill, AsDictMixin

from forecast.dto import GeoAddress

MULTI_SPACE_RE = re.compile(r'\s+')

# https://developers.google.com/maps/documentation/geocoding/requests-geocoding#GeocodingResponses
FORMATTED_ADDR_DATA_PATH = ['formatted_address']
ADDR_COMPONENTS_DATA_PATH = ['address_components']
LATITUDE_DATA_PATH = ['geometry', 'location', 'lat']
LONGITUDE_DATA_PATH = ['geometry', 'location', 'lng']


@dataclass
class GeoCodeResult(AsDictMixin):
    """
    Dataclass for geocode result
    """
    components: List[Dict[str, Any]]
    country: str    # ISO 3166-1 alpha-2 country code
    formatted_addr: str
    latitude: float
    longitude: float


class GoogleMapsClient:
    """
    Singleton instance of the Google Maps client
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        return cls._instance


def geocode_address(address: List[str]) -> Tuple[GeoAddress, Dict[str, Any]]:
    """
    Geocode an address
    :param address: list of address fields
    :return: tuple of geocoded address and raw geocode result
    """
    # https://developers.google.com/maps/documentation/geocoding/overview
    # https://github.com/googlemaps/google-maps-services-python

    addr = list(map(lambda a: MULTI_SPACE_RE.sub(' ', a), address))

    # request geocode from Google Maps
    if settings.CACHED_GEOCODE_RESULT:
        # HACK: use a cached result
        geocode_result = json.loads(settings.CACHED_GEOCODE_RESULT)
    else:
        geocode_result = GoogleMapsClient().geocode(', '.join(addr))

    is_valid = len(geocode_result) > 0
    result = geocode_result[0] if is_valid else {}

    # determine country
    addr_components = dict_drill(
        result, *ADDR_COMPONENTS_DATA_PATH, default=[]).value

    country = next(
        filter(lambda c: 'country' in c['types'], addr_components),
        {'short_name': ''})['short_name']

    geo_addr = GeoAddress(
        formatted_address=dict_drill(
            result, *FORMATTED_ADDR_DATA_PATH, default='').value,
        country=country,
        lat=dict_drill(
            result, *LATITUDE_DATA_PATH, default=0.0).value,
        lng=dict_drill(
            result, *LONGITUDE_DATA_PATH, default=0.0).value,
        is_valid=is_valid
    )

    return geo_addr, GeoCodeResult(
        components=addr_components,
        country=country,
        formatted_addr=geo_addr.formatted_address,
        latitude=geo_addr.lat,
        longitude=geo_addr.lng
    )
