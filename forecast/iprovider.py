"""
Interface for forecast providers
"""
# MIT License
#
# Copyright (c) 2023 Ian Buttimer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from abc import ABC, abstractmethod


class IProvider(ABC):
    """
    Interface for forecast providers
    """

    @abstractmethod
    def location_url(self, latitude: str, longitude: str, **kwargs) -> str:
        """
        Get forecast url for a location

        :param latitude: Latitude of the location
        :param longitude: Longitude of the location
        :return: url
        """

    @abstractmethod
    def get_forecast(self, location: str, **kwargs) -> dict:
        """
        Get forecast for a location

        :param location: Location to get forecast for
        :param kwargs: Additional arguments
        :return: Forecast
        """
