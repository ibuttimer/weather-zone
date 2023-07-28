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
from datetime import datetime, tzinfo, timezone
from http import HTTPStatus
import json
from typing import Dict, Tuple

import requests
import xmltodict

from django.conf import settings

from base import get_request_headers
from utils import dict_drill, ensure_list

from forecast import Forecast, ForecastEntry, GeoAddress, Location, Provider

from .constants import (
    DATETIME_FORMAT, CREATED_PATH, FORECAST_DATA_PATH, DATATYPE_ATTRIB,
    FROM_ATTRIB, TO_ATTRIB, FORECAST_PROP, LOCATION_PROP, ALTITUDE_PROP,
    LATITUDE_PROP, LONGITUDE_PROP, UNIT_ATTRIB, VALUE_ATTRIB, NAME_ATTRIB,
    DEG_ATTRIB, MPS_ATTRIB, PERCENT_ATTRIB, LITERAL_MARKER, PERCENT_LITERAL,
    PROBABILITY_ATTRIB, NUM_ATTRIB, ID_ATTRIB, OLD_ID_PROP, VARIANTS_PROP,
    TEMPERATURE_TAG, WIND_DIRECTION_TAG, WIND_SPEED_TAG, WIND_GUST_TAG,
    HUMIDITY_TAG, PRECIPITATION_TAG, SYMBOL_TAG
)
from .legends import LegendStore, load_legends
from .provider import (
    LocationforecastProvider, ForecastAttrib, NO_LEGEND_ADDENDUM,
    DAY_LEGEND_ADDENDUM, NIGHT_LEGEND_ADDENDUM
)


DARK_LEGEND_OFFSET = 100    # offset of dark variant legends

# Met Eireann forecast attributes
ME_ATTRIBUTES = {
    TEMPERATURE_TAG: ForecastAttrib(
        ForecastEntry.TEMPERATURE_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
    WIND_DIRECTION_TAG: [
        ForecastAttrib(ForecastEntry.WIND_DIR_KEY, DEG_ATTRIB, DEG_ATTRIB),
        ForecastAttrib(ForecastEntry.WIND_CARDINAL_KEY, None, NAME_ATTRIB)
    ],
    WIND_SPEED_TAG: ForecastAttrib(
        ForecastEntry.WIND_SPEED_KEY, MPS_ATTRIB, MPS_ATTRIB),
    WIND_GUST_TAG: ForecastAttrib(
        ForecastEntry.WIND_GUST_KEY, MPS_ATTRIB, MPS_ATTRIB),
    HUMIDITY_TAG: ForecastAttrib(
        ForecastEntry.HUMIDITY_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
    PRECIPITATION_TAG: [
        ForecastAttrib(ForecastEntry.PRECIPITATION_KEY, UNIT_ATTRIB, VALUE_ATTRIB),
        ForecastAttrib(ForecastEntry.PRECIPITATION_PROB_KEY, PERCENT_LITERAL,
                       PROBABILITY_ATTRIB)
    ],
    SYMBOL_TAG: [
        ForecastAttrib(ForecastEntry.SYMBOL_KEY, ID_ATTRIB, NUM_ATTRIB),
        ForecastAttrib(ForecastEntry.ALT_TEXT_KEY, ID_ATTRIB, ID_ATTRIB),
    ]
}


class MetEireannProvider(LocationforecastProvider):
    """
    Forecast provider
    """
    from_q: str     # From date/time query parameter
    to_q: str       # To date/time query parameter

    def __init__(self, name: str, friendly_name: str, url: str,
                 lat_q: str, lng_q: str, from_q: str, to_q: str):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param from_q: From date/time query parameter
        :param to_q: To date/time query parameter
        """
        super().__init__(name, friendly_name, url, lat_q, lng_q, ME_ATTRIBUTES)
        self.from_q = from_q
        self.to_q = to_q

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
        params = super().url_params(lat, lng)
        for q, v in [(self.from_q, start), (self.to_q, end)]:
            if v is not None:
                params[q] = v.strftime('%Y-%m-%dT%H:%M')
        return params

    def get_id_variant(self, legend: Dict) -> Tuple[int, str]:
        """
        Get the id and variant addendum for icon filename
        :param legend: legend to get id and variant from
        :return: tuple of id and variant addendum
        """
        addendum = DAY_LEGEND_ADDENDUM if legend.get(VARIANTS_PROP, None) \
            else NO_LEGEND_ADDENDUM
        old_id = int(legend.get(OLD_ID_PROP))
        if old_id > DARK_LEGEND_OFFSET:
            old_id -= DARK_LEGEND_OFFSET
            assert old_id > 0
            addendum = NIGHT_LEGEND_ADDENDUM
        return old_id, addendum
