"""
Met Eireann forecast provider
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
import os
from collections import namedtuple
from datetime import datetime, tzinfo, timezone
from http import HTTPStatus
import json

import requests
import xmltodict

from django.conf import settings

from utils import dict_drill, ensure_list

from forecast.dto import Forecast, GeoAddress, ForecastEntry
from forecast.provider import Provider


BASE_LEGENDS_URL = os.path.join(settings.BASE_DIR, 'data/met-eireann/legends.json')
PATCH_LEGENDS_URL = os.path.join(settings.BASE_DIR, 'data/met-eireann/me-legends.json')
DARK_LEGEND_OFFSET = 100    # offset of dark variant legends
NO_LEGEND_ADDENDUM = ''
DAY_LEGEND_ADDENDUM = 'd'
NIGHT_LEGEND_ADDENDUM = 'n'
WEATHER_ICON_URL = 'img/weather_icons/'

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
CREATED_PATH = ['weatherdata', '@created']
FORECAST_DATA_PATH = ['weatherdata', 'product', 'time']
DATATYPE_ATTRIB = '@datatype'
FROM_ATTRIB = '@from'
TO_ATTRIB = '@to'
LOCATION_PROP = 'location'
UNIT_ATTRIB = '@unit'
VALUE_ATTRIB = '@value'
DEG_ATTRIB = '@deg'
MPS_ATTRIB = '@mps'
PERCENT_ATTRIB = '@percent'
LITERAL_MARKER = '$'
PERCENT_LITERAL = f'{LITERAL_MARKER}percent'
PROBABILITY_ATTRIB = '@probability'
NUM_ATTRIB = '@number'
ID_ATTRIB = '@id'

# Met Eireann keys (standardised to lower case)
ME_TEMPERATURE_KEY = 'temperature'
ME_WIND_DIRECTION_KEY = 'winddirection'
ME_WIND_SPEED_KEY = 'windspeed'
ME_WIND_GUST_KEY = 'windgust'
ME_HUMIDITY_KEY = 'humidity'
ME_PRECIPITATION_KEY = 'precipitation'
ME_SYMBOL_KEY = 'symbol'

#                                  Forecast key, unit attrib, value attrib
MeAttrib = namedtuple('MeAttrib', ['key', 'unit', 'value'])

ME_ATTRIBUTES = {
    ME_TEMPERATURE_KEY: MeAttrib(
        ForecastEntry.TEMPERATURE_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
    ME_WIND_DIRECTION_KEY: MeAttrib(
        ForecastEntry.WIND_DIR_KEY, DEG_ATTRIB, DEG_ATTRIB),
    ME_WIND_SPEED_KEY: MeAttrib(
        ForecastEntry.WIND_SPEED_KEY, MPS_ATTRIB, MPS_ATTRIB),
    ME_WIND_GUST_KEY: MeAttrib(
        ForecastEntry.WIND_GUST_KEY, MPS_ATTRIB, MPS_ATTRIB),
    ME_HUMIDITY_KEY: MeAttrib(
        ForecastEntry.HUMIDITY_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
    ME_PRECIPITATION_KEY: [
        MeAttrib(ForecastEntry.PRECIPITATION_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
        MeAttrib(ForecastEntry.PRECIPITATION_PROB_KEY, PERCENT_LITERAL,
                 PROBABILITY_ATTRIB)
    ],
    ME_SYMBOL_KEY: MeAttrib(
        ForecastEntry.SYMBOL_KEY, ID_ATTRIB, ID_ATTRIB),
}

# attrib unit to display
ME_UNITS = {
    'celsius': '°C',
    'percent': '%',
    PERCENT_ATTRIB: '%',
    MPS_ATTRIB: 'm/s',
    'hPa': 'hPa',
    'mm': 'mm',
    DEG_ATTRIB: '°',
    NUM_ATTRIB: '',
    ID_ATTRIB: '',
}
ATTRIB_IS_UNIT = [
    MPS_ATTRIB, PERCENT_ATTRIB, DEG_ATTRIB
]


class MetEireannProvider(Provider):
    """
    Forecast provider
    """
    lat_q: str      # Latitude query parameter
    lng_q: str      # Longitude query parameter
    from_q: str     # From date/time query parameter
    to_q: str       # To date/time query parameter
    legends: dict   # Legends

    def __init__(self, name: str, url: str, lat_q: str, lng_q: str,
                 from_q: str, to_q: str):
        """
        Constructor

        :param name: Name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param from_q: From date/time query parameter
        :param to_q: To date/time query parameter
        """
        super().__init__(name, url)
        self.lat_q = lat_q
        self.lng_q = lng_q
        self.from_q = from_q
        self.to_q = to_q
        self.legends = load_legends()

    def url_params(self, lat: float, lng: float, start: datetime = None,
                   end: datetime = None, **kwargs) -> dict:
        """
        Get query params of forecast url for a location

        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param start: forecast start date; default is current time
        :param end: forecast end date; default is end of available forecast
        :return: url
        """
        # https://data.gov.ie/dataset/met-eireann-weather-forecast-api
        # http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast?lat=<LATITUDE>;long=<LONGITUDE>;from=2018-11-10T02:00;to=2018-11-12T12:00
        params = {
            self.lat_q: lat,
            self.lng_q: lng,
        }
        for q, v in [(self.from_q, start), (self.to_q, end)]:
            if v is not None:
                params[q] = v.strftime('%Y-%m-%dT%H:%M')
        return params

    def get_geo_forecast(self, geo_address: GeoAddress, start: datetime = None,
                         end: datetime = None, **kwargs) -> Forecast:
        """
        Get forecast for a location using geographic coordinates

        :param geo_address:
        :param start: forecast start date; default is current time
        :param end: forecast end date; default is end of available forecast
        :param kwargs: Additional arguments
        :return: Forecast
        """
        params = self.url_params(
            geo_address.lat, geo_address.lng, start=start, end=end, **kwargs)

        # request forecast
        forecast = Forecast(geo_address)
        forecast.provider = self.name
        try:
            response = requests.get(
                self.url, params=params, timeout=settings.REQUEST_TIMEOUT)
            if response.status_code == HTTPStatus.OK:
                parse_forecast(response.text, forecast)

                # get icon for each forecast entry
                for entry in forecast.time_series:
                    entry.icon = self.get_icon(entry.symbol)

        except requests.exceptions.RequestException as e:
            print(e)

        return forecast

    def get_icon(self, legend: str) -> str:
        """
        Get the icon for a forecast

        :param legend: Legend to retrieve
        :return: Legend
        """
        # "sun": {
        #     "desc_en": "Sun",
        #     "old_id": "1",
        #     "variants": [
        #         "day",
        #         "night",
        #         "polartwilight"
        #     ]
        # },
        # The original and variant legends may be connected via the 'old_id'
        # field; variant 'old_id' values are the original 'old_id' + 100
        legend = legend.lower()
        if legend not in self.legends:
            raise ValueError(f"Legend '{legend}' not found")
        entry = self.legends.get(legend)
        addendum = DAY_LEGEND_ADDENDUM if entry.get('variants', None) \
            else NO_LEGEND_ADDENDUM
        old_id = int(entry.get('old_id'))
        if old_id > DARK_LEGEND_OFFSET:
            old_id -= DARK_LEGEND_OFFSET
            addendum = NIGHT_LEGEND_ADDENDUM

        return f"{WEATHER_ICON_URL}{old_id:02d}{addendum}.svg"

    def __str__(self):
        return f"{self.name}, {self.url}"


def parse_forecast(data: str, forecast: Forecast) -> Forecast:
    """
    Parse a forecast

    :param data: forecast data to parse
    :param forecast: Forecast to update
    :return: Parsed forecast
    """
    units_set = set()
    data = xmltodict.parse(data)

    # get created date/time
    now: datetime = datetime.now(tz=timezone.utc)
    forecast.created = extract_datetime(
        dict_drill(data, *CREATED_PATH,
                   default=now.strftime(DATETIME_FORMAT)).value
    )
    # get forecast data
    forecast_entries = {}
    forecast_data = dict_drill(data, *FORECAST_DATA_PATH, default=[])
    for entry in forecast_data.value if forecast_data.found else []:
        if entry.get(DATATYPE_ATTRIB, None) != 'forecast':
            continue
        # get forecast date/time
        from_dt: datetime = extract_datetime(entry.get(FROM_ATTRIB))
        to_dt: datetime = extract_datetime(entry.get(TO_ATTRIB))
        # get forecast entry based on end date/time so that instant forecasts
        # (temp/wind/etc.) are added to the end of period forecasts
        # (rain/symbol)
        f_cast = forecast_entries.get(
            to_dt, ForecastEntry.of_period(start=from_dt, end=to_dt))
        forecast_entries[to_dt] = f_cast

        for fc_key, fc_value in entry.get(LOCATION_PROP, {}).items():
            # e.g. fc_key
            #   "@altitude", "@latitude", "@longitude", "temperature", ...
            #      fc_value
            #    "43",  "53.6106",  "-6.1970", {
            #       "@id": "TTT", "@unit": "celsius", "@value": "16.1"
            #    }, ... }
            fc_key = fc_key.lower()
            if fc_key not in ME_ATTRIBUTES:
                continue

            for me_attrib in ensure_list(ME_ATTRIBUTES.get(fc_key)):

                # set unit
                if me_attrib.key not in units_set:
                    # get attrib unit
                    unit = me_attrib.unit   # default, attrib key is the unit
                    if unit.startswith(LITERAL_MARKER):
                        # attrib value is the unit
                        unit = unit[len(LITERAL_MARKER):]
                    elif unit not in ATTRIB_IS_UNIT:
                        # attrib value is the unit
                        unit = fc_value.get(unit)
                    forecast.units[me_attrib.key] = ME_UNITS.get(unit)
                    units_set.add(me_attrib.key)

                # process attrib value
                value = fc_value.get(me_attrib.value)
                if me_attrib.key in ForecastEntry.FLOAT_KEYS:
                    value = float(value if value else 0)
                setattr(f_cast, me_attrib.key, value)

        # set time series
        forecast.time_series = sorted(
            forecast_entries.values(), key=lambda x: x.end
        )

    return forecast


def load_legends() -> dict:
    """
    Load legends
    :return:
    """
    # load legends from json file
    with open(BASE_LEGENDS_URL, 'r') as f:
        legends = json.load(f)

    # patch legends from json file
    with open(PATCH_LEGENDS_URL, 'r') as f:
        patch_legends = json.load(f)
        legends.update(patch_legends)

    for key in legends.keys():
        if not key.islower():
            legends[key.lower()] = legends.pop(key)

    return legends


def extract_datetime(dt: str) -> datetime:
    """
    Extract datetime from string

    :param dt: Date/time string
    :return: Datetime
    """
    return datetime.strptime(dt, DATETIME_FORMAT)
