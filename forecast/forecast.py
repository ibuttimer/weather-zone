"""
Forecasting module
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
from datetime import datetime
from typing import Optional

from .dto import GeoAddress, Forecast
from .registry import Registry


def generate_forecast(
        geo_address: GeoAddress, start: datetime = None,
        end: datetime = None, provider: str = None) -> Forecast:
    """
    Get a forecast
    :param geo_address: geographic address
    :param start: forecast start date; default is current time
    :param end: forecast end date; default is end of available forecast
    :param provider: forecast provider; default is all providers
    :return: Forecast
    """
    registry = Registry.get_registry()
    if provider is None:
        # get all providers
        for forcaster in registry.providers.values():
            loc_forecast = forcaster.get_geo_forecast(geo_address, start, end)

    else:
        # get specific provider
        loc_forecast = registry.providers.get(provider) \
            .get_geo_forecast(geo_address, start, end)

    return loc_forecast
