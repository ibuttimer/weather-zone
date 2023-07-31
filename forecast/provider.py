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

from .iprovider import IProvider


class Provider(IProvider, ABC):
    """
    Forecast provider
    """
    name: str       # Name of provider
    friendly_name: str   # user friendly of provider
    url: str        # URL of provider
    tz: ZoneInfo    # timezone

    def __init__(self, name: str, friendly_name: str, url: str, tz: str):
        """
        Constructor

        :param name: Name of provider
        :param friendly_name: User friendly name of provider
        :param url: URL of provider
        :param tz: Timezone identifier of provider
        """
        self.name = name
        self.friendly_name = friendly_name
        self.url = url
        self.tz = ZoneInfo(tz or "UTC")

    def __str__(self):
        return f"{self.name}, {self.url}"

    def get_name(self) -> str:
        """
        Get the name of the provider

        :return: Name of provider
        """
        return self.name

    def get_url(self) -> str:
        """
        Get the url of the provider

        :return: URL of provider
        """
        return self.url

    def read_cached_resp(self, filepath: str) -> str:
        """
        Read cached response

        :param filepath: Path to cached response
        :return: Cached response
        """
        response = None
        with open(filepath, 'r') as f:
            response = f.read()
        return response
