"""
Data transfer objects for forecast module
"""
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
from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Tuple, Set

from utils import AsDictMixin
from addresses.constants import (
    COUNTRY_FIELD as ADDR_COUNTRY_FIELD,
    FORMATTED_ADDR_FIELD as ADDR_FORMATTED_ADDR_FIELD,
    LATITUDE_FIELD as ADDR_LATITUDE_FIELD,
    LONGITUDE_FIELD as ADDR_LONGITUDE_FIELD,
    PLACE_ID_FIELD as ADDR_PLACE_ID_FIELD,
    GLOBAL_PLUS_CODE_FIELD as ADDR_GLOBAL_PLUS_CODE_FIELD
)
from ..beaufort import Beaufort
from ..enums import AttribRowTypes

from ..constants import (
    FORMATTED_ADDR_FIELD as GEOCODE_FORMATTED_ADDR_FIELD,
    COUNTRY_FIELD as GEOCODE_COUNTRY_FIELD,
    LATITUDE_FIELD as GEOCODE_LATITUDE_FIELD,
    LONGITUDE_FIELD as GEOCODE_LONGITUDE_FIELD,
    PLACE_ID_FIELD as GEOCODE_PLACE_ID_FIELD,
    GLOBAL_PLUS_CODE_FIELD as GEOCODE_GLOBAL_PLUS_CODE_FIELD,
)


AttribRow = namedtuple('AttribRow',
                       # display text or callable, attribute name,
                       #                        format function, type
                       ['text', 'attribute', 'format_fxn', 'type'],
                       defaults=[None, None, None, None])
""" Tuple to hold attribute row data for forecast display """


@dataclass
class GeoAddress(AsDictMixin):
    """
    Geocoded address
    """
    FORMATTED_ADDRESS_FIELD = 'formatted_address'
    COUNTRY_FIELD = 'country'
    LAT_FIELD = 'lat'
    LNG_FIELD = 'lng'
    PLACE_ID_FIELD = 'place_id'
    GLOBAL_PLUS_CODE_FIELD = 'global_plus_code'

    IS_VALID_FIELD = 'is_valid'

    _DEFAULT_VALS = {
        FORMATTED_ADDRESS_FIELD: '',
        COUNTRY_FIELD: '',
        LAT_FIELD: 0.0,
        LNG_FIELD: 0.0,
        PLACE_ID_FIELD: '',
        GLOBAL_PLUS_CODE_FIELD: '',
        IS_VALID_FIELD: False
    }

    _GEOADDRESS_ADDR_KEYS = {
        FORMATTED_ADDRESS_FIELD: ADDR_FORMATTED_ADDR_FIELD,
        COUNTRY_FIELD: ADDR_COUNTRY_FIELD,
        LAT_FIELD: ADDR_LATITUDE_FIELD,
        LNG_FIELD: ADDR_LONGITUDE_FIELD,
        PLACE_ID_FIELD: ADDR_PLACE_ID_FIELD,
        GLOBAL_PLUS_CODE_FIELD: ADDR_GLOBAL_PLUS_CODE_FIELD
    }

    _GEOCODERESULT_ADDR_KEYS = {
        FORMATTED_ADDRESS_FIELD: GEOCODE_FORMATTED_ADDR_FIELD,
        COUNTRY_FIELD: GEOCODE_COUNTRY_FIELD,
        LAT_FIELD: GEOCODE_LATITUDE_FIELD,
        LNG_FIELD: GEOCODE_LONGITUDE_FIELD,
        PLACE_ID_FIELD: GEOCODE_PLACE_ID_FIELD,
        GLOBAL_PLUS_CODE_FIELD: GEOCODE_GLOBAL_PLUS_CODE_FIELD
    }

    formatted_address: str
    country: str        # ISO 3166-1 alpha-2 country code
    lat: float
    lng: float
    place_id: str
    global_plus_code: str
    is_valid: bool

    @staticmethod
    def default_vals() -> Dict[str, Any]:
        """
        Get the default values for a GeoAddress map
        :return: map of keys and corresponding default values
        """
        return GeoAddress._DEFAULT_VALS.copy()

    @staticmethod
    def dict_keys() -> List[Tuple[str, Any]]:
        """
        Get the keys for a GeoAddress map
        :return: list of keys and default values
        """
        return list(GeoAddress.default_vals().items())

    @staticmethod
    def from_dict(address: Dict[str, Any]) -> 'GeoAddress':
        """
        Convert a map to a GeoAddress
        :param address: map of GeoAddress
        :return: GeoAddress
        """
        return GeoAddress(**{
            k: address.get(k, v) for k, v in GeoAddress.dict_keys()
        })

    @staticmethod
    def _from_address(address: Any, keys_map: dict) -> 'GeoAddress':
        """
        Convert an Address to a GeoAddress
        :param address: Address model instance or GeoCodeResult
        :return: GeoAddress
        """
        addr_dict = dict(GeoAddress.dict_keys())
        for geo_k, addr_k in keys_map.items():
            addr_dict[geo_k] = getattr(address, addr_k)
        addr_dict[GeoAddress.IS_VALID_FIELD] = True
        return GeoAddress(**addr_dict)

    @staticmethod
    def from_address(address: Any) -> 'GeoAddress':
        """
        Convert an Address to a GeoAddress
        :param address: Address model instance
        :return: GeoAddress
        """
        return GeoAddress._from_address(
            address, GeoAddress._GEOADDRESS_ADDR_KEYS)

    @staticmethod
    def from_geocode_result(address: 'GeoCodeResult') -> 'GeoAddress':
        """
        Convert a GeoCodeResult to a GeoAddress
        :param address: GeoCodeResult
        :return: GeoAddress
        """
        return GeoAddress._from_address(
            address, GeoAddress._GEOCODERESULT_ADDR_KEYS)

    @staticmethod
    def empty_obj() -> 'GeoAddress':
        """
        Generate an empty GeoAddress
        :return: GeoAddress
        """
        return GeoAddress.from_dict(dict(GeoAddress.dict_keys()))


@dataclass
class Location(GeoAddress):
    """
    Geocoded location
    """
    ALTITUDE_FIELD = 'altitude'

    altitude: float

    @staticmethod
    def dict_keys() -> List[Tuple[str, Any]]:
        """
        Get the keys for a Location map
        :return: list of keys and default values
        """
        return GeoAddress.dict_keys() + [
            (Location.ALTITUDE_FIELD, 0.0)
        ]

    @staticmethod
    def from_dict(location: Dict[str, Any]) -> 'Location':
        """
        Convert a map to a Location
        :param location: map of Location
        :return: Location
        """
        return Location(**{
            k: location.get(k, v) for k, v in Location.dict_keys()
        })

    @staticmethod
    def empty_obj() -> 'Location':
        """
        Generate an empty Location
        :return: Location
        """
        return Location.from_dict({
            k: v for k, v in Location.dict_keys()
        })


@dataclass
class ForecastEntry:
    """
    Forecast entry
    """
    START_KEY = "start"
    END_KEY = "end"
    TEMPERATURE_KEY = "temperature"
    WIND_DIR_KEY = "wind_dir"
    WIND_CARDINAL_KEY = "wind_cardinal"
    WIND_DIR_ICON_KEY = "wind_dir_icon"
    WIND_SPEED_KEY = "wind_speed"
    WIND_SPEED_ICON_KEY = "wind_speed_icon"
    WIND_GUST_KEY = "wind_gust"
    BEAUFORT_KEY = "beaufort"
    HUMIDITY_KEY = "humidity"
    PRECIPITATION_KEY = "precipitation"
    PRECIPITATION_PROB_KEY = "precipitation_prob"
    SYMBOL_KEY = "symbol"
    ALT_TEXT_KEY = "alt_text"
    ICON_KEY = "icon"

    # keys that are floats
    FLOAT_KEYS = [
        TEMPERATURE_KEY, WIND_DIR_KEY, WIND_SPEED_KEY, WIND_GUST_KEY,
        HUMIDITY_KEY, PRECIPITATION_KEY, PRECIPITATION_PROB_KEY
    ]
    # keys that are ints
    INT_KEYS = [
        BEAUFORT_KEY
    ]

    start: datetime  # start date/time
    end: datetime  # end date/time
    temperature: float  # temperature
    wind_dir: float  # wind direction
    wind_cardinal: str  # wind cardinal direction
    wind_dir_icon: str  # wind direction icon
    wind_speed: float  # wind speed
    wind_speed_icon: str  # wind speed icon
    wind_gust: float  # wind gust
    beaufort: int  # beaufort scale
    humidity: float  # humidity
    precipitation: float  # precipitation
    precipitation_prob: float  # precipitation probability
    symbol: str  # symbol
    alt_text: str  # alternative text
    icon: str  # icon

    @staticmethod
    def of_period(start: datetime, end: datetime):
        """
        Create a forecast entry for a period
        :param start: start date
        :param end: end date
        :return: forecast entry
        """
        return ForecastEntry(
            start=start,
            end=end,
            temperature=0.0,
            wind_dir=0.0,
            wind_cardinal='',
            wind_dir_icon='',
            wind_speed=0.0,
            wind_speed_icon='',
            wind_gust=0.0,
            beaufort=0,
            humidity=0.0,
            precipitation=0.0,
            precipitation_prob=0.0,
            symbol='',
            alt_text='',
            icon=''
        )

    @property
    def is_instant(self) -> bool:
        """
        Is this an instant forecast?
        :return: True if instant, False otherwise
        """
        return self.start and self.start == self.end


@dataclass
class ImageData:
    """
    Image data
    """
    url: str
    alt_text: str


class Forecast:
    """
    Forecast
    """
    created: datetime  # date/time forecast was created
    address: GeoAddress  # address forecast is for
    provider: str  # name of forecast provider
    units: Dict[str, str]  # units used in forecast; key is ForecastEntry key
    time_series: List[ForecastEntry]  # time series forecast
    # attribute series forecast, key is display name, value is list of values
    attrib_series: Dict[str, List[Any]]
    cached: bool  # is this a cached forecast?
    forecast_attribs: Set[str]  # set of available forecast attributes
    missing_attribs: Set[str]   # set of missing attributes

    def __init__(self, address: GeoAddress, provider: str = ''):
        self.address = address
        self.created = datetime.now()
        self.provider = provider
        self.units = {}
        self.time_series = []
        self.attrib_series: {}
        self.cached = False
        self.forecast_attribs = set()
        self.missing_attribs = set()

    def set_units(self, units: dict):
        """
        Set the units
        :param units: Units to set
        """
        self.units = units

    def get_units(self, key: str) -> str:
        """
        Get the units for the specified key
        :param key: key to get units for
        :return: units
        """
        return self.units.get(key, '')

    def set_attrib_series(self, display_items: List[AttribRow]):
        """
        Set the attribute series, i.e. a series of the display name and a
        list of values for each specified attribute.
        e.g. [['Temperature', 12.3, 14.5, 16.7], ['Humidity', 0.5, 0.6, 0.7]]

        :param display_items: Attribute rows to generate series
        Note 1: the AttribRow text field may be a
                Callable[[Forecast, AttribRow, Any, int, Any], str].
             2: the AttribRow format_fxn field may be a
                Callable[[Forecast, AttribRow, Any], str].
        """
        self.attrib_series = []
        for item in display_items:

            # skip if attribute to display is not part of forecast, or
            # expected attribute was not provided
            # if (item.attribute not in self.forecast_attribs or
            #         item.attribute in self.missing_attribs):
            if item.attribute in self.missing_attribs:
                continue

            row = [item.text(self, item) if callable(item.text) else item.text]
            prev_value = None
            for idx, entry in enumerate(self.time_series):
                value = getattr(entry, item.attribute)
                if item.format_fxn:
                    # pass in the forecast, AttribRow, value, index and
                    # previous value to
                    # Callable[[Forecast, AttribRow, Any, int, Any], str]
                    display_value = (
                        item.format_fxn(self, item, value, idx, prev_value))
                elif item.type == AttribRowTypes.WEATHER_ICON:
                    display_value = ImageData(value, entry.alt_text)
                elif item.type == AttribRowTypes.WIND_DIR_ICON:
                    display_value = ImageData(value, entry.wind_cardinal)
                elif item.type == AttribRowTypes.WIND_SPEED_ICON:
                    display_value = ImageData(
                        value, Beaufort.from_beaufort(
                            entry.beaufort).alt_translations_kmh)
                else:
                    display_value = value

                row.append(display_value)
                prev_value = value

            self.attrib_series.append(row)
