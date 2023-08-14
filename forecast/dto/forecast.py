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
from typing import List, Dict, Any, Tuple, Set, Callable, Optional

from utils import AsDictMixin

AttribRow = namedtuple('AttribRow',
                       # display text or callable, attribute name,
                       #                        format function, type
                       ['text', 'attribute', 'format_fxn', 'type'],
                       defaults=[None, None, None, None])
""" Tuple to hold attribute row data for forecast display """

# AttribRow types
TYPE_HDR = 'hdr'                # header
TYPE_WEATHER_ICON = 'img_wi'    # weather icon image
TYPE_WIND_DIR_ICON = 'img_wd'   # wind direction icon image


@dataclass
class GeoAddress(AsDictMixin):
    """
    Geocoded address
    """
    FORMATTED_ADDRESS_FIELD = 'formatted_address'
    COUNTRY_FIELD = 'country'
    LAT_FIELD = 'lat'
    LNG_FIELD = 'lng'
    IS_VALID_FIELD = 'is_valid'

    formatted_address: str
    country: str        # ISO 3166-1 alpha-2 country code
    lat: float
    lng: float
    is_valid: bool

    @staticmethod
    def dict_keys() -> List[Tuple[str, Any]]:
        """
        Get the keys for a GeoAddress map
        :return: list of keys and default values
        """
        return [
            (GeoAddress.FORMATTED_ADDRESS_FIELD, ''),
            (GeoAddress.COUNTRY_FIELD, ''),
            (GeoAddress.LAT_FIELD, 0.0),
            (GeoAddress.LNG_FIELD, 0.0),
            (GeoAddress.IS_VALID_FIELD, False)
        ]

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
    WIND_GUST_KEY = "wind_gust"
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

    start: datetime  # start date/time
    end: datetime  # end date/time
    temperature: float  # temperature
    wind_dir: float  # wind direction
    wind_cardinal: str  # wind cardinal direction
    wind_dir_icon: str  # wind direction icon
    wind_speed: float  # wind speed
    wind_gust: float  # wind gust
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
            wind_gust=0.0,
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
                elif item.type == TYPE_WEATHER_ICON:
                    display_value = ImageData(value, entry.alt_text)
                elif item.type == TYPE_WIND_DIR_ICON:
                    display_value = ImageData(value, entry.wind_cardinal)
                else:
                    display_value = value

                row.append(display_value)
                prev_value = value

            self.attrib_series.append(row)
