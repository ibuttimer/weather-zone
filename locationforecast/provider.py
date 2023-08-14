"""
Locationforecast forecast provider
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
from dataclasses import dataclass
from datetime import datetime, tzinfo, timezone
from http import HTTPStatus
import json
from typing import Dict, Tuple

import requests
import xmltodict

from django.conf import settings

from base import get_request_headers
from utils import dict_drill, ensure_list

from broker import ServiceType
from forecast import (
    Forecast, ForecastEntry, GeoAddress, Location, Provider,
    TYPE_WEATHER_ICON, TYPE_WIND_DIR_ICON, WeatherWarnings
)

from .constants import (
    CREATED_PATH, FORECAST_DATA_PATH, DATATYPE_ATTRIB,
    FROM_ATTRIB, TO_ATTRIB, FORECAST_PROP, LOCATION_PROP, ALTITUDE_PROP,
    LATITUDE_PROP, LONGITUDE_PROP, UNIT_ATTRIB, VALUE_ATTRIB, NAME_ATTRIB,
    DEG_ATTRIB, MPS_ATTRIB, PERCENT_ATTRIB, LITERAL_MARKER, PERCENT_LITERAL,
    PROBABILITY_ATTRIB, NUM_ATTRIB, ID_ATTRIB, OLD_ID_PROP, VARIANTS_PROP,
    ATTRIB_MARKER
)
from .legends import LegendStore, load_legends

NO_LEGEND_ADDENDUM = ''
DAY_LEGEND_ADDENDUM = 'd'
NIGHT_LEGEND_ADDENDUM = 'n'
WEATHER_ICON_URL = 'img/weather_icons/{old_id:02d}{addendum}.svg'
WIND_DIR_ICON_URL = 'img/wind_icons/cardinal-{name}.png'


@dataclass
class ForecastAttrib:
    """
    Forecast attribute
    """
    key: str    # Forecast key
    unit: str   # Unit attribute name
    value: str  # Value attribute name
    dflt_unit: str  # default unit attribute value or name for symbol lookup

    @staticmethod
    def of_unit_val(key: str, dflt_unit: str):
        """
        Create a ForecastAttrib with unit and value attributes
        e.g. <temperature unit="celsius" value="10.0"/>

        :param key: Forecast key
        :param dflt_unit: Default unit
        :return: ForecastAttrib
        """
        return ForecastAttrib(key, UNIT_ATTRIB, VALUE_ATTRIB, dflt_unit)

    @staticmethod
    def of_no_unit(key: str, attrib: str):
        """
        Create a ForecastAttrib with unit and value attributes
        e.g. wind direction name
        <windDirection id="dd" deg="262.3" name="W"></windDirection>

        :param key: Forecast key
        :param attrib: Attribute name 
        :return: ForecastAttrib
        """
        return ForecastAttrib(key, None, attrib, None)

    @staticmethod
    def of_attrib_unit(key: str, attrib: str, dflt_unit: str):
        """
        Create a ForecastAttrib with attribute name as unit
        e.g. wind direction degree
        <windDirection id="dd" deg="262.3" name="W"></windDirection>

        :param key: Forecast key
        :param attrib: Attribute name 
        :param dflt_unit: Default unit
        :return: ForecastAttrib
        """
        return ForecastAttrib(key, attrib, attrib, dflt_unit)


# default unit attribute value or attribute name for unit symbol lookup
DFLT_TEMP_UNIT = 'celsius'
DLFT_PERCENT_UNIT = 'percent'
DLFT_SPEED_UNIT = MPS_ATTRIB
DLFT_PRESSURE_UNIT = 'hPa'
DLFT_HEIGHT_UNIT = 'mm'
DLFT_DEG_UNIT = DEG_ATTRIB

# attrib unit to display lookup
ATTRIB_UNITS = {
    'celsius': '°C',
    # Note: 'percent' is a special case
    'percent': '%',         # value of 'value' attribute in tag
    PERCENT_ATTRIB: '%',    # attribute name in tag
    MPS_ATTRIB: 'm/s',
    'hPa': 'hPa',
    'mm': 'mm',
    DEG_ATTRIB: '°',
}

# fields to extract the location from
LOCATION_FIELDS = {
    ALTITUDE_PROP: Location.ALTITUDE_FIELD,
    LATITUDE_PROP: Location.LAT_FIELD,
    LONGITUDE_PROP: Location.LNG_FIELD,
}

# cardinal directions for which there are images and their corresponding
# degrees
CARDINAL_DIRECTIONS = {
    0: 'n', 180: 's', 90: 'e', 270: 'w',
    45: 'ne', 315: 'nw', 135: 'se', 225: 'sw'
}
DIR_COUNT = len(CARDINAL_DIRECTIONS)    # number of cardinal directions
ARC_PER_DIR = 360 / DIR_COUNT       # degrees per cardinal direction segment
HALF_ARC_PER_DIR = ARC_PER_DIR / 2  # mid-point of cardinal direction segment


class LocationforecastProvider(Provider):
    """
    Forecast provider
    """
    LATITUDE_PROP = 'lat_q'
    LONGITUDE_PROP = 'lng_q'

    lat_q: str  # Latitude query parameter
    lng_q: str  # Longitude query parameter
    attributes: Dict[str, ForecastAttrib]  # forecast parsing attributes
    cached_result: str  # cached result; used for development

    legends: LegendStore  # Legends

    def __init__(self, name: str, friendly_name: str, url: str,
                 lat_q: str, lng_q: str, tz: str, country: str,
                 attributes: Dict[str, ForecastAttrib]):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        :param attributes: Attributes to use to parse forecast
        """
        super().__init__(
            name, friendly_name, url, tz, country, ServiceType.FORECAST)
        self.lat_q = lat_q
        self.lng_q = lng_q
        self.attributes = attributes
        self.cached_result = None
        LocationforecastProvider.init_legends()

    @staticmethod
    def init_legends() -> LegendStore:
        """
        Initialise the legend store, if not already done

        :return: LegendStore
        """
        if not hasattr(LocationforecastProvider, 'legends'):
            LocationforecastProvider.legends = load_legends()
        return LocationforecastProvider.legends

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
        # https://api.met.no/weatherapi/locationforecast/2.0/documentation
        # https://api.met.no/weatherapi/locationforecast/2.0/classic?lat=59.93&lon=10.72&altitude=90
        return {
            self.lat_q: lat,
            self.lng_q: lng,
        }

    def get_geo_forecast(self, geo_address: GeoAddress, start: datetime = None,
                         end: datetime = None, **kwargs) -> Forecast:
        """
        Get forecast for a location using geographic coordinates

        :param geo_address:
        :param start: forecast start date (server timezone);
                    default is current time
        :param end: forecast end date (server timezone);
                    default is end of available forecast
        :param kwargs: Additional arguments
        :return: Forecast
        """
        # adjust start and end dates to provider timezone
        if start:
            start = start.astimezone(self.tz)
        if end:
            end = end.astimezone(self.tz)

        params = self.url_params(
            geo_address.lat, geo_address.lng, start=start, end=end, **kwargs)
        weather_icon_attrib = kwargs.get(TYPE_WEATHER_ICON, None)
        wind_dir_icon_attrib = kwargs.get(TYPE_WIND_DIR_ICON, None)

        # request forecast
        forecast = Forecast(geo_address, provider=self.friendly_name)

        forecast_resp = None
        if self.cached_result:
            forecast_resp = self.read_cached_resp(self.cached_result)
            forecast.cached = len(forecast_resp) > 0
        else:
            try:
                response = requests.get(
                    self.url, params=params, headers=get_request_headers(),
                    timeout=settings.REQUEST_TIMEOUT)
                if response.status_code == HTTPStatus.OK:
                    forecast_resp = response.text

            except requests.exceptions.RequestException as e:
                print(e)

        if forecast_resp:
            parse_forecast(forecast_resp, forecast, self.attributes,
                           start=start, end=end)

            # get icons for each ForecastEntry
            for entry in forecast.time_series:
                # forecast summary icon
                entry.icon = self.get_icon(entry.symbol)
                # wind direction icon
                entry.wind_dir_icon = self.get_wind_dir_icon(
                    entry.wind_cardinal, entry.wind_dir)

            if len(forecast.time_series) > 0:
                if weather_icon_attrib:
                    forecast.forecast_attribs.add(weather_icon_attrib)
                if wind_dir_icon_attrib:
                    forecast.forecast_attribs.add(wind_dir_icon_attrib)

        return forecast

    def get_warnings(self, **kwargs) -> WeatherWarnings:
        """
        Get weather warnings

        :return: WeatherWarnings
        """
        raise NotImplementedError(
            f'{self.name} does not support weather warnings')

    def get_id_variant(self, legend: Dict) -> Tuple[int, str]:
        """
        Get the id and variant addendum for icon filename
        :param legend: legend to get id and variant from
        :return: tuple of id and variant addendum
        """
        addendum = DAY_LEGEND_ADDENDUM if legend.get(VARIANTS_PROP, None) \
            else NO_LEGEND_ADDENDUM
        old_id = int(legend.get(OLD_ID_PROP))
        return old_id, addendum

    def get_icon(self, legend: str) -> str:
        """
        Get the icon for a forecast

        :param legend: Legend to retrieve
        :return: icon url
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
        if not self.legends.key_exists(legend):
            raise ValueError(f"Legend '{legend}' not found")
        entry = self.legends.get(legend)
        old_id, addendum = self.get_id_variant(entry)

        return WEATHER_ICON_URL.format(old_id=old_id, addendum=addendum)

    def get_wind_dir_icon(self, name: str, degrees: float) -> str:
        """
        Get the icon for wind direction

        :param name: wind direction cardinal name
        :param degrees: wind direction in degrees
        :return: icon url
        """
        name = name.lower()
        if name not in CARDINAL_DIRECTIONS.values():
            # determine cardinal direction from degrees
            name = CARDINAL_DIRECTIONS[
                (int((degrees + HALF_ARC_PER_DIR) / ARC_PER_DIR) % DIR_COUNT)
                * ARC_PER_DIR
            ]

        return WIND_DIR_ICON_URL.format(name=name)


def parse_forecast(data: str, forecast: Forecast,
                   attributes: Dict[str, ForecastAttrib],
                   start: datetime = None, end: datetime = None) -> Forecast:
    """
    Parse a forecast

    :param data: forecast data to parse
    :param forecast: Forecast to update
    :param attributes: Attributes to use to parse forecast
    :param start: forecast start date (provider timezone);
                    default is current time
    :param end: forecast end date (provider timezone);
                    default is end of available forecast
    :return: Parsed forecast
    """
    units_set = set()
    location_set = set()
    location = Location.empty_obj()

    data = xmltodict.parse(data)

    # get created date/time
    now: str = datetime.now(tz=timezone.utc).isoformat()
    forecast.created = datetime.fromisoformat(
        dict_drill(data, *CREATED_PATH, default=now).value
    )
    # set of all expected attributes
    forecast.forecast_attribs = set(
        a.key for row in attributes.values() for a in ensure_list(row)
    )
    # add end time as forecast entry based on end date/time and always included
    forecast.forecast_attribs.add(ForecastEntry.END_KEY)
    units_set.add(ForecastEntry.END_KEY)

    start_dt_utc = start.astimezone(timezone.utc) if start else None
    end_dt_utc = end.astimezone(timezone.utc) if end else None

    # get forecast data
    forecast_entries = {}
    forecast_data = dict_drill(data, *FORECAST_DATA_PATH, default=[])
    for entry in forecast_data.value if forecast_data.found else []:
        if entry.get(DATATYPE_ATTRIB, None) != FORECAST_PROP:
            continue
        # get forecast date/time
        from_dt: datetime = datetime.fromisoformat(entry.get(FROM_ATTRIB))
        to_dt: datetime = datetime.fromisoformat(entry.get(TO_ATTRIB))

        from_dt_utc = from_dt.astimezone(timezone.utc)
        to_dt_utc = to_dt.astimezone(timezone.utc)
        if not settings.IGNORE_FORECAST_WINDOW:
            # exclude if entry date/time range outside start/end range
            if start_dt_utc:
                if to_dt_utc < start_dt_utc:
                    continue
            if end_dt_utc:
                if from_dt_utc > end_dt_utc or to_dt_utc > end_dt_utc:
                    continue

        # get forecast entry based on end date/time so that instant forecasts
        # (temp/wind/etc.) are added to the end of period forecasts
        # (rain/symbol)
        to_dt = to_dt.astimezone(tz=None)   # server timezone
        from_dt = from_dt.astimezone(tz=None)   # server timezone
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
            if fc_key in LOCATION_FIELDS.keys() and fc_key not in location_set:
                # set location fields (all float)
                setattr(location, LOCATION_FIELDS[fc_key],
                        float(fc_value if fc_value else 0))
                location_set.add(fc_key)

            if fc_key not in attributes:
                continue

            # set attributes
            for me_attrib in ensure_list(attributes.get(fc_key)):

                # set units as specified by the forecast data
                if me_attrib.key not in units_set:
                    # get attrib unit
                    unit = me_attrib.unit   # default, attrib key is the unit
                    if unit:
                        if unit.startswith(LITERAL_MARKER):
                            # attrib value is the unit,
                            # (literal marker was prepended as identifier)
                            unit = unit[len(LITERAL_MARKER):]
                        elif unit == UNIT_ATTRIB:
                            # unit attrib value is the unit
                            unit = fc_value.get(unit)
                        # else attrib name is the unit
                        forecast.units[me_attrib.key] = ATTRIB_UNITS.get(unit)
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

    forecast.missing_attribs = forecast.forecast_attribs - units_set

    return forecast
