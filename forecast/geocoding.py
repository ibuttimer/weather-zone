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
from typing import List, Tuple, Dict, Any, TypeVar, Optional, Callable
import re
import googlemaps

from django.conf import settings

from utils import dict_drill, AsDictMixin, ensure_list

from forecast.dto import GeoAddress

from .constants import (
    COMPONENTS_FIELD, COUNTRY_FIELD, FORMATTED_ADDR_FIELD, LATITUDE_FIELD,
    LONGITUDE_FIELD, PLACE_ID_FIELD, GLOBAL_PLUS_CODE_FIELD,
    COMPOUND_PLUS_CODE_FIELD, RES_TYPE_FIELD
)

MULTI_SPACE_RE = re.compile(r'\s+')

# https://developers.google.com/maps/documentation/geocoding/requests-geocoding#GeocodingResponses
FORMATTED_ADDR_DATA_PATH = ['formatted_address']
ADDR_COMPONENTS_DATA_PATH = ['address_components']
PLACE_ID_PATH = ['place_id']
RESULT_TYPE_PATH = ['types']
GLOBAL_PLUS_CODE_PATH = ['plus_code', 'global_code']
COMPOUND_PLUS_CODE_PATH = ['plus_code', 'compound_code']
LATITUDE_DATA_PATH = ['geometry', 'location', 'lat']
LONGITUDE_DATA_PATH = ['geometry', 'location', 'lng']

AddrResult = TypeVar('AddrResult', bound=Dict[str, Any])
""" Address result type; '{
         "address_components": [...],
         "formatted_address": .. }'
"""
AddrComponents = TypeVar('AddrComponents', bound=List[Dict[str, Any]])


@dataclass
class GeoCodeResult(AsDictMixin):
    """
    Dataclass for geocode result corresponding to address fields of Address
    model
    """
    LONG_NAME = 'long_name'
    SHORT_NAME = 'short_name'

    # types of result component
    STREET_NUMBER = 'street_number'
    STREET_ADDRESS = 'street_address'
    NEIGHBORHOOD = 'neighborhood'
    POSTAL_CODE = 'postal_code'
    ROUTE = 'route'
    LOCALITY = 'locality'
    STATE = 'administrative_area_level_1'
    COUNTRY = 'country'

    COMPONENTS_FIELD = COMPONENTS_FIELD
    COUNTRY_FIELD = COUNTRY_FIELD
    FORMATTED_ADDR_FIELD = FORMATTED_ADDR_FIELD
    LATITUDE_FIELD = LATITUDE_FIELD
    LONGITUDE_FIELD = LONGITUDE_FIELD
    PLACE_ID_FIELD = PLACE_ID_FIELD
    GLOBAL_PLUS_CODE_FIELD = GLOBAL_PLUS_CODE_FIELD
    COMPOUND_PLUS_CODE_FIELD = COMPOUND_PLUS_CODE_FIELD
    RES_TYPE_FIELD = RES_TYPE_FIELD

    components: List[Dict[str, Any]]
    country: str    # ISO 3166-1 alpha-2 country code
    formatted_addr: str
    latitude: float
    longitude: float
    place_id: str
    global_plus_code: str
    compound_plus_code: str
    res_type: str   # type of result, e.g. 'street_address'

    @classmethod
    def first_result(cls, results: List[AddrResult]) -> Optional[AddrResult]:
        """
        Get the first result from the client results
        :param results: list of results
        :return: result or None if no results
        """
        return results[0] if len(results) > 0 else None

    @classmethod
    def result_of_type(cls, results: List[AddrResult],
                       res_type: str) -> Optional[AddrResult]:
        """
        Get the first result of the type specified from the client results
        :param results: list of results
        :param res_type: type of result, e.g. 'street_address'
        :return: result or None if not found
        """
        results = list(filter(
            lambda r: res_type in dict_drill(
                r, *RESULT_TYPE_PATH, default=[]).value, results))
        return results[0] if len(results) > 0 else None

    @classmethod
    def street_address_result(
            cls, results: List[AddrResult]) -> Optional[AddrResult]:
        """
        Get the 'street_address' result from the client results
        :param results: list of results
        :return: result or None if no results
        """
        return cls.result_of_type(results, cls.STREET_ADDRESS)

    @classmethod
    def postcode_result(
            cls, results: List[AddrResult]) -> Optional[AddrResult]:
        """
        Get the 'postal_code' result from the client results
        :param results: list of results
        :return: result or None if no results
        """
        return cls.result_of_type(results, cls.POSTAL_CODE)

    @classmethod
    def locality_result(
            cls, results: List[AddrResult]) -> Optional[AddrResult]:
        """
        Get the 'locality' result from the client results
        :param results: list of results
        :return: result or None if no results
        """
        return cls.result_of_type(results, cls.LOCALITY)

    @staticmethod
    def from_client_result(
            results: List[AddrResult],
            select_funcs: List[
                Callable[[List[AddrResult]], Optional[AddrResult]]
            ]) -> Optional['GeoCodeResult']:
        """
        Create a GeoCodeResult from the client result provided
        :param results: client result
        :param select_funcs: list of functions to select the result to convert
        :return: GeoCodeResult instance or None if no result
        """
        result = None
        for func in ensure_list(select_funcs):
            result = func(results)
            if result is not None:
                break

        if result is not None:
            components = dict_drill(
                result, *ADDR_COMPONENTS_DATA_PATH, default=[]).value
            res_type = dict_drill(
                result, *RESULT_TYPE_PATH, default=[]).value
            result = GeoCodeResult(
                components=components,
                country=GeoCodeResult.country_code_from_components(components),
                formatted_addr=dict_drill(
                    result, *FORMATTED_ADDR_DATA_PATH, default='').value,
                latitude=dict_drill(
                    result, *LATITUDE_DATA_PATH, default=0.0).value,
                longitude=dict_drill(
                    result, *LONGITUDE_DATA_PATH, default=0.0).value,
                place_id=dict_drill(
                    result, *PLACE_ID_PATH, default='').value,
                global_plus_code=dict_drill(
                    result, *GLOBAL_PLUS_CODE_PATH, default='').value,
                compound_plus_code=dict_drill(
                    result, *COMPOUND_PLUS_CODE_PATH, default='').value,
                res_type=res_type[0] if len(res_type) > 0 else ''
            )
        return result

    @property
    def country_name(self) -> str:
        """
        Get the name of the country for this GeoCodeResult
        :return: country name
        """
        return GeoCodeResult.country_name_from_components(self.components)

    @property
    def country_code(self) -> str:
        """
        Get the ISO 3166-1 alpha-2 country code for this GeoCodeResult
        :return: country code
        """
        return GeoCodeResult.country_code_from_components(self.components)

    @staticmethod
    def data_from_components(components: AddrComponents, comp_type: str,
                             attrib: str = LONG_NAME) -> str:
        """
        Extract data from the components
        :param components: list of components
        :param comp_type: component type, see
         https://developers.google.com/maps/documentation/geocoding/requests-geocoding#Types
        :param attrib: attribute to extract, default 'long_name'
        https://developers.google.com/maps/documentation/geocoding/requests-geocoding#GeocodingResponses
        :return: data
        """
        return next(
            filter(lambda c: comp_type in c['types'], components),
            {attrib: ''})[attrib]

    @staticmethod
    def country_code_from_components(components: AddrComponents) -> str:
        """
        Extract the ISO 3166-1 alpha-2 country code from the components
        :param components: list of components
        :return: country code
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.COUNTRY, attrib=GeoCodeResult.SHORT_NAME)

    @staticmethod
    def country_name_from_components(components: AddrComponents) -> str:
        """
        Extract the country name from the components
        :param components: list of components
        :return: country code
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.COUNTRY)

    @staticmethod
    def postcode_from_components(components: AddrComponents) -> str:
        """
        Extract the postcode from the components
        :param components: list of components
        :return: postcode
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.POSTAL_CODE)

    @staticmethod
    def state_from_components(components: AddrComponents) -> str:
        """
        Extract the state from the components;
        'administrative_area_level_1' indicates a first-order civil entity
        below the country level, e.g. a state in the United States
        :param components: list of components
        :return: postcode
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.STATE)

    @staticmethod
    def locality_from_components(components: AddrComponents) -> str:
        """
        Extract the locality from the components;
        'locality' indicates an incorporated city or town political entity
        :param components: list of components
        :return: postcode
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.LOCALITY)

    @staticmethod
    def line1_from_components(components: AddrComponents) -> str:
        """
        Extract the street number and route from the components
        'street_number' indicates the precise street number
        'route' indicates a named route
        :param components: list of components
        :return: postcode
        """
        street_num = GeoCodeResult.data_from_components(
            components, GeoCodeResult.STREET_NUMBER)
        route = GeoCodeResult.data_from_components(
            components, GeoCodeResult.ROUTE)
        return f'{street_num} {route}' if street_num else route

    @staticmethod
    def line2_from_components(components: AddrComponents) -> str:
        """
        Extract the neighbourhood from the components
        'neighborhood' indicates a named neighborhood
        :param components: list of components
        :return: postcode
        """
        return GeoCodeResult.data_from_components(
            components, GeoCodeResult.NEIGHBORHOOD)


class GoogleMapsClient:
    """
    Singleton instance of the Google Maps client
    """
    _instance: Optional[googlemaps.Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        return cls._instance

    def geocode(self, address=None, place_id=None, components=None, bounds=None,
                region=None, language=None) -> List[AddrResult]:
        """
        Geocode an address.
        See :py:meth:`googlemaps.Client.geocode` for more information.
        :param address: The address to geocode.
        :param place_id: A textual identifier that uniquely identifies a place,
            returned from a Places search.
        :param components: A component filter for which you wish to obtain a
            geocode, for example:
            ``{'administrative_area': 'TX','country': 'US'}``
        :param bounds: The bounding box of the viewport within which to bias
            geocode results more prominently.
        :param region: The region code, specified as a ccTLD
            ("top-level domain") two-character value.
        :param language: The language in which to return results.
        :return: list of geocoding results.
        """
        return self._instance.geocode(
            address=address, place_id=place_id, components=components,
            bounds=bounds, region=region, language=language)


def geocode_address(address: List[str],
                    *args) -> Tuple[GeoAddress, GeoCodeResult]:
    """
    Geocode an address
    :param address: list of address fields
    :return: tuple of geocoded address and geocode result
    """
    # https://developers.google.com/maps/documentation/geocoding/overview
    # https://github.com/googlemaps/google-maps-services-python

    addr = list(map(lambda a: MULTI_SPACE_RE.sub(' ', a), address))

    # request geocode from Google Maps
    if settings.CACHED_GEOCODE_RESULT:
        # HACK: use a cached result
        geocode_results = json.loads(settings.CACHED_GEOCODE_RESULT)
    else:
        geocode_results = GoogleMapsClient().geocode(', '.join(addr))

    # get result in decreasing order of specificity
    geocode_res = GeoCodeResult.from_client_result(
        geocode_results, [
            GeoCodeResult.street_address_result,
            GeoCodeResult.postcode_result,
            GeoCodeResult.locality_result,
            GeoCodeResult.first_result
        ])

    geo_addr = GeoAddress.from_geocode_result(geocode_res) \
        if geocode_res is not None else GeoAddress.empty_obj()

    return geo_addr, geocode_res
