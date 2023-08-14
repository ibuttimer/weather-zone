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
    CREATED_PATH, FORECAST_DATA_PATH, DATATYPE_ATTRIB,
    FROM_ATTRIB, TO_ATTRIB, FORECAST_PROP, LOCATION_PROP, ALTITUDE_PROP,
    LATITUDE_PROP, LONGITUDE_PROP, UNIT_ATTRIB, VALUE_ATTRIB, NAME_ATTRIB,
    DEG_ATTRIB, MPS_ATTRIB, BEAUFORT_ATTRIB, PERCENT_ATTRIB, LITERAL_MARKER,
    PERCENT_LITERAL, PROBABILITY_ATTRIB, NUM_ATTRIB, ID_ATTRIB, OLD_ID_PROP,
    VARIANTS_PROP, TEMPERATURE_TAG, WIND_DIRECTION_TAG, WIND_SPEED_TAG,
    WIND_GUST_TAG, HUMIDITY_TAG, PRECIPITATION_TAG, SYMBOL_TAG
)
from .legends import LegendStore, load_legends
from .provider import (
    LocationforecastProvider, ForecastAttrib, NO_LEGEND_ADDENDUM,
    DAY_LEGEND_ADDENDUM, NIGHT_LEGEND_ADDENDUM,
    DFLT_TEMP_UNIT, DLFT_PERCENT_UNIT, DLFT_SPEED_UNIT, DLFT_PRESSURE_UNIT,
    DLFT_HEIGHT_UNIT, DLFT_DEG_UNIT
)


# Met Norway forecast attributes
MN_ATTRIBUTES = {
    TEMPERATURE_TAG: ForecastAttrib.of_unit_val(
        ForecastEntry.TEMPERATURE_KEY, DFLT_TEMP_UNIT),
    WIND_DIRECTION_TAG: [
        ForecastAttrib.of_attrib_unit(
            ForecastEntry.WIND_DIR_KEY, DEG_ATTRIB, DLFT_DEG_UNIT),
        ForecastAttrib.of_no_unit(
            ForecastEntry.WIND_CARDINAL_KEY, NAME_ATTRIB)
    ],
    WIND_SPEED_TAG: [
        ForecastAttrib.of_attrib_unit(
            ForecastEntry.WIND_SPEED_KEY, MPS_ATTRIB, DLFT_SPEED_UNIT),
        ForecastAttrib.of_no_unit(
            ForecastEntry.BEAUFORT_KEY, BEAUFORT_ATTRIB),
    ],
    WIND_GUST_TAG: ForecastAttrib.of_attrib_unit(
        ForecastEntry.WIND_GUST_KEY, MPS_ATTRIB, DLFT_SPEED_UNIT),
    HUMIDITY_TAG: ForecastAttrib.of_unit_val(
        ForecastEntry.HUMIDITY_KEY, DLFT_PERCENT_UNIT),
    PRECIPITATION_TAG: [
        ForecastAttrib.of_unit_val(
            ForecastEntry.PRECIPITATION_KEY, DLFT_HEIGHT_UNIT),
        # Met Norway doesn't provide precipitation probability in
        # locationforecast classic ver 2.0
    ],
    SYMBOL_TAG: [
        ForecastAttrib.of_no_unit(ForecastEntry.SYMBOL_KEY, NUM_ATTRIB),
        ForecastAttrib.of_no_unit(ForecastEntry.ALT_TEXT_KEY, ID_ATTRIB),
    ]
}


class MetNorwayClassicProvider(LocationforecastProvider):
    """
    Forecast provider
    """

    def __init__(self, name: str, friendly_name: str, url: str,
                 lat_q: str, lng_q: str, tz: str, country: str):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param lat_q: Latitude query parameter
        :param lng_q: Longitude query parameter
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        """
        super().__init__(
            name, friendly_name, url, lat_q, lng_q, tz, country, MN_ATTRIBUTES)
