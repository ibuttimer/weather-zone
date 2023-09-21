"""
Interface for forecast providers
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
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from broker import ServiceType
from .dto import Forecast, GeoAddress, WeatherWarnings


class IProvider(ABC):
    """
    Interface for forecast providers
    """

    stype: Optional[ServiceType]      # service type

    def __init__(self):
        self.stype = None

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def get_warnings(self, **kwargs) -> WeatherWarnings:
        """
        Get weather warnings

        :return: WeatherWarnings
        """
