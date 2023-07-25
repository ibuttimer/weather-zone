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
from typing import List, Dict, Any

AttribRow = namedtuple('AttribRow',
                       # display text, attribute name, format function, type
                       ['text', 'attribute', 'format_fxn', 'type'],
                       defaults=[None, None, None, None])


@dataclass
class GeoAddress:
    """
    Geocoded address
    """
    formatted_address: str
    lat: float
    lng: float
    is_valid: bool

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert a GeoAddress to a map
        :param address: GeoAddress to convert
        :return: map of GeoAddress
        """
        return {
            'formatted_address': self.formatted_address,
            'lat': self.lat,
            'lng': self.lng,
            'is_valid': self.is_valid
        }

    @staticmethod
    def from_dict(address: Dict[str, Any]) -> 'GeoAddress':
        """
        Convert a map to a GeoAddress
        :param address: map of GeoAddress
        :return: GeoAddress
        """
        return GeoAddress(
            formatted_address=address.get('formatted_address', ''),
            lat=address.get('lat', 0.0),
            lng=address.get('lng', 0.0),
            is_valid=address.get('is_valid', False)
        )


@dataclass
class Location(GeoAddress):
    """
    Geocoded location
    """
    altitude: float


@dataclass
class ForecastEntry():
    """
    Forecast entry
    """
    START_KEY = "start"
    END_KEY = "end"
    TEMPERATURE_KEY = "temperature"
    WIND_DIR_KEY = "wind_dir"
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
    units: Dict[str, str]  # units used in forecast
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

    def set_attrib_series(self, attrib_rows: List[AttribRow]):
        """
        Set the attribute series, i.e. a series of the display name and a
        list of values for each specified attribute.
        e.g. [['Temperature', 12.3, 14.5, 16.7], ['Humidity', 0.5, 0.6, 0.7]]
        :param attrib_rows: Attribute rows to generate series
        """
        self.attrib_series = []
        for item in attrib_rows:
            row = [item.text]
            for entry in self.time_series:
                value = getattr(entry, item.attribute)
                if item.format_fxn:
                    value = item.format_fxn(value)
                elif item.type == 'img':
                    value = ImageData(value, entry.symbol)
                row.append(value)
            self.attrib_series.append(row)
