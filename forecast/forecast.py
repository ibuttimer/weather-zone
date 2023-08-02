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
from typing import Optional, List

from .dto import GeoAddress, Forecast
from .provider import ProviderType
from .registry import Registry


def generate_forecast(
        geo_address: GeoAddress, start: datetime = None,
        end: datetime = None, provider: str = None, **kwargs) -> List[Forecast]:
    """
    Get a list of forecasts
    :param geo_address: geographic address
    :param start: forecast start date; default is current time
    :param end: forecast end date; default is end of available forecast
    :param provider: name of forecast provider; default is all providers
    :param kwargs: Additional arguments
    :return: Forecast
    """
    registry = Registry.get_registry()
    forecasts = []
    providers = [provider] if provider is not None \
        else registry.provider_names(ptype=ProviderType.FORECAST)

    for provider in providers:
        forecasts.append(
            registry.get(provider).get_geo_forecast(
                geo_address, start, end, **kwargs)
        )

    return forecasts
