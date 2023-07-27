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
from typing import List, Dict, Any, Tuple

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
class GeoAddress:
    """
    Geocoded address
    """
    FORMATTED_ADDRESS_FIELD = 'formatted_address'
    LAT_FIELD = 'lat'
    LNG_FIELD = 'lng'
    IS_VALID_FIELD = 'is_valid'

    formatted_address: str
    lat: float
    lng: float
    is_valid: bool

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert a GeoAddress to a map
        :return: map of GeoAddress
        """
        return {
            GeoAddress.FORMATTED_ADDRESS_FIELD: self.formatted_address,
            GeoAddress.LAT_FIELD: self.lat,
            GeoAddress.LNG_FIELD: self.lng,
            GeoAddress.IS_VALID_FIELD: self.is_valid
        }

    @staticmethod
    def dict_keys() -> List[Tuple[str, Any]]:
        """
        Get the keys for a GeoAddress map
        :return: list of keys and default values
        """
        return [
            (GeoAddress.FORMATTED_ADDRESS_FIELD, ''),
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
        return GeoAddress.from_dict({
            k: v for k, v in GeoAddress.dict_keys()
        })


@dataclass
class Location(GeoAddress):
    """
    Geocoded location
    """
    ALTITUDE_FIELD = 'altitude'

    altitude: float

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert a Location to a map
        :return: map of Location
        """
        data = super().as_dict()
        data.update({
            Location.ALTITUDE_FIELD: self.altitude
        })
        return data

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

    def __init__(self, address: GeoAddress):
        self.address = address
        self.created = datetime.now()
        self.provider = ''
        self.units = {}
        self.time_series = []
        self.attrib_series: {}

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

    def set_attrib_series(self, attrib_rows: List[AttribRow]):
        """
        Set the attribute series, i.e. a series of the display name and a
        list of values for each specified attribute.
        e.g. [['Temperature', 12.3, 14.5, 16.7], ['Humidity', 0.5, 0.6, 0.7]]

        :param attrib_rows: Attribute rows to generate series
        Note 1: the AttribRow text field may be a
                Callable[[Forecast, AttribRow], str].
             2: the AttribRow format_fxn field may be a
                Callable[[Forecast, AttribRow, Any], str].
        """
        self.attrib_series = []
        for item in attrib_rows:
            row = [item.text(self, item) if callable(item.text) else item.text]
            for entry in self.time_series:
                value = getattr(entry, item.attribute)
                if item.format_fxn:
                    # pass in the forecast, the AttribRow and the value
                    value = item.format_fxn(self, item, value)
                elif item.type == TYPE_WEATHER_ICON:
                    value = ImageData(value, entry.symbol)
                elif item.type == TYPE_WIND_DIR_ICON:
                    value = ImageData(value, entry.wind_cardinal)
                row.append(value)
            self.attrib_series.append(row)
