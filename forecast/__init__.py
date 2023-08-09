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
    ADDRESS_ROUTE_NAME, LAT_LONG_ROUTE_NAME, QUERY_PROVIDER,
    QUERY_PARAM_LAT, QUERY_PARAM_LONG, QUERY_PARAM_FROM, QUERY_PARAM_TO
)
from .dto import (
    Forecast, ForecastEntry, GeoAddress, Location,
    TYPE_WEATHER_ICON, TYPE_WIND_DIR_ICON,
    WeatherWarnings, WarningEntry
)
from .enums import Severity, Category
from .iprovider import IProvider, ProviderType
from .loader import load_provider
from .misc import ALL_PROVIDERS
from .provider import Provider
from .registry import Registry
from .signals import registry_open


__all__ = [
    'ADDRESS_ROUTE_NAME',
    'LAT_LONG_ROUTE_NAME',
    'QUERY_PROVIDER',
    'QUERY_PARAM_LAT',
    'QUERY_PARAM_LONG',
    'QUERY_PARAM_FROM',
    'QUERY_PARAM_TO',

    'Forecast',
    'ForecastEntry',
    'GeoAddress',
    'Location',
    'TYPE_WEATHER_ICON',
    'TYPE_WIND_DIR_ICON',
    'WeatherWarnings',
    'WarningEntry',

    'Severity',
    'Category',

    'IProvider',
    'ProviderType',

    'load_provider',

    'ALL_PROVIDERS',

    'Provider',

    'Registry',

    'registry_open',
]
