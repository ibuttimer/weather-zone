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
from .constants import (
    DASH_ROUTE_NAME, ADDRESS_ROUTE_NAME, LAT_LONG_ROUTE_NAME, QUERY_PROVIDER,
    QUERY_PARAM_LAT, QUERY_PARAM_LONG, QUERY_PARAM_FROM, QUERY_PARAM_TO,
    ALL_PROVIDERS, GEOCODE_SERVICE, GEOCODE_ADDRESS_FUNC
)
from .dto import (
    Forecast, ForecastEntry, GeoAddress, Location,
    WeatherWarnings, WarningEntry
)
from .enums import Severity, Category, AttribRowTypes
from .geocoding import GeoCodeResult
from .help import forecast_help
from .iprovider import IProvider
from .loader import load_provider, ProviderCfgEntry
from .provider import Provider
from .registry import Registry, get_provider_info
from .signals import registry_open


__all__ = [
    'DASH_ROUTE_NAME',
    'ADDRESS_ROUTE_NAME',
    'LAT_LONG_ROUTE_NAME',
    'QUERY_PROVIDER',
    'QUERY_PARAM_LAT',
    'QUERY_PARAM_LONG',
    'QUERY_PARAM_FROM',
    'QUERY_PARAM_TO',
    'ALL_PROVIDERS',
    'GEOCODE_SERVICE',
    'GEOCODE_ADDRESS_FUNC',

    'Forecast',
    'ForecastEntry',
    'GeoAddress',
    'Location',
    'WeatherWarnings',
    'WarningEntry',

    'Severity',
    'Category',
    'AttribRowTypes',

    'GeoCodeResult',

    'forecast_help',

    'IProvider',

    'load_provider',
    'ProviderCfgEntry',

    'Provider',

    'Registry',
    'get_provider_info',

    'registry_open',
]
