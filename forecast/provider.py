"""
Forecast provider
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
from abc import ABC
from zoneinfo import ZoneInfo

from django_countries.fields import Country

from .iprovider import IProvider, ProviderType


class Provider(IProvider, ABC):
    """
    Forecast provider
    """
    NAME_PROP = 'name'
    FRIENDLY_NAME_PROP = 'friendly_name'
    URL_PROP = 'url'
    TZ_PROP = 'tz'
    COUNTRY_PROP = 'country'
    PTYPE_PROP = 'ptype'

    name: str               # Name of provider
    friendly_name: str      # user friendly of provider
    url: str                # URL of provider
    tz: ZoneInfo            # timezone
    country: Country        # country
    ptype: ProviderType     # provider type

    def __init__(self, name: str, friendly_name: str, url: str, tz: str,
                 country: str, ptype: ProviderType = ProviderType.UNKNOWN):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param tz: Timezone identifier of provider
        :param country: ISO 3166-1 alpha-2 country code of provider
        :param ptype: type of Provider
        """
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.tz = ZoneInfo(tz or "UTC")
        self.country = Country(country)
        self.ptype = ptype

    @staticmethod
    def read_cached_resp(filepath: str) -> str:
        """
        Read cached response

        :param filepath: Path to cached response
        :return: Cached response
        """
        with open(filepath, 'r') as f:
            response = f.read()
        return response

    def is_forecast(self) -> bool:
        """
        Is this a forecast provider

        :return: True if forecast provider, otherwise False
        """
        return self.ptype in [
            ProviderType.FORECAST, ProviderType.FORECAST_WARNING
        ]

    def is_warning(self) -> bool:
        """
        Is this a warning provider

        :return: True if warning provider, otherwise False
        """
        return self.ptype in [
            ProviderType.WARNING, ProviderType.FORECAST_WARNING
        ]

    def is_country_supported(self, country: str) -> bool:
        """
        Is the country supported by this provider

        :param country: ISO 3166-1 alpha-2 country code
        :return: True if supported, otherwise False
        """
        return self.country.code == country

    def __str__(self):
        return f"{self.name}, {self.country.code}, {self.ptype}, {self.url}"
