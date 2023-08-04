"""
Weather warnings provider
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
from forecast.dto import TYPE_WEATHER_ICON
from utils import dict_drill, ensure_list

from forecast import (
    Forecast, ForecastEntry, GeoAddress, Location, Provider, ProviderType,
)

from .regions import RegionStore, load_regions




class WarningsProvider(Provider):
    """
    Weather warnings provider
    """
    cached_result: str  # cached result; used for development

    regions: RegionStore  # Legends

    def __init__(self, name: str, friendly_name: str, url: str, tz: str,
                 country: str):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        """
        super().__init__(
            name, friendly_name, url, tz, country, ProviderType.WARNING)
        self.cached_result = None
        WarningsProvider.init_regions()

    @staticmethod
    def init_regions() -> RegionStore:
        """
        Initialise the legend store, if not already done

        :return: RegionStore
        """
        if not hasattr(WarningsProvider, 'regions'):
            WarningsProvider.regions = load_regions()
        return WarningsProvider.regions

    def url_params(self, **kwargs) -> dict:
        """
        Get query params of weather warnings url

        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param start: start date; default is current time
        :param end: end date; default is end of available forecast
        :return: url
        """
        return {}

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
        raise NotImplementedError(f'{self.name} does not support forecasting')
